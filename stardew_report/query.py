"""Direct lxml queries used by the ported rules; no browser, scripts or network.

The small HTML control tree supplies upstream default prediction ranges. XML
selectors are compiled and cached. Report markup is parsed only for formatting.
"""

from functools import lru_cache
from html import escape
import re
from lxml import etree, html
from cssselect import GenericTranslator
from .runtime import U, Array, Fn, Obj, string, truth


@lru_cache(maxsize=2048)
def selector_xpath(selector, include_self=False):
    # Sizzle matches this ancestor spelling against lowercase characters.
    # Keep other names exact: saves can contain both animals and Animals.
    selector = re.sub(r"\bCharacters(?=\s*(?:>|\s))", "characters", selector)
    path = GenericTranslator().css_to_xpath(
        selector, prefix="descendant-or-self::" if include_self else "descendant::"
    )
    path = re.sub(
        r"attribute::\*\[name\(\) = 'xmlns:([^']+)'\]",
        r"namespace::*[name() = '\1']",
        path,
    )
    return etree.XPath(path)


def select(element, selector, include_self=False):
    return selector_xpath(selector, include_self)(element)


def inner_html(element):
    return escape(element.text or "", quote=False) + "".join(
        etree.tostring(c, encoding="unicode", method="html", with_tail=True)
        for c in element
    )


def set_html(element, value):
    for child in list(element):
        element.remove(child)
    element.text = None
    # lxml.html avoids creating a browser DOM for every intermediate result.
    fragment = html.fragment_fromstring(string(value), create_parent="div")
    element.text = fragment.text
    for child in list(fragment):
        element.append(child)


class Node:
    def __init__(self, element, document):
        self.element = element
        self.document = document

    def js_get(self, key):
        if key == "innerHTML":
            return inner_html(self.element)
        if key == "nodeName":
            return self.element.tag
        if key in ("checked", "selected", "disabled"):
            return key in self.element.attrib
        if key == "value":
            return Query([self.element], self.document).val()
        return self.element.get(key, U)

    def js_put(self, key, value):
        if key == "innerHTML":
            set_html(self.element, value)
        else:
            Query([self.element], self.document).prop(key, value)


class Query:
    def __init__(self, elements, document, is_document=False):
        self.elements = elements
        self.document = document
        self.is_document = is_document

    def js_get(self, key):
        if key == "length":
            return len(self.elements)
        if key.isdigit():
            i = int(key)
            return (
                Node(self.elements[i], self.document) if i < len(self.elements) else U
            )
        if key == "is":
            return self.is_
        return getattr(self, key, U)

    def find(self, selector):
        found = []
        seen = set()
        for el in self.elements:
            for child in select(el, string(selector), self.is_document):
                if child not in seen:
                    found.append(child)
                    seen.add(child)
        return Query(found, self.document)

    def children(self, selector=U):
        found = [c for el in self.elements for c in el if isinstance(c.tag, str)]
        if selector is not U:
            found = [c for c in found if c in select(c, string(selector), True)]
        return Query(found, self.document)

    def first(self):
        return Query(self.elements[:1], self.document)

    def text(self):
        return "".join("".join(el.itertext()) for el in self.elements)

    def html(self, value=U):
        if value is U:
            return inner_html(self.elements[0]) if self.elements else U
        for el in self.elements:
            set_html(el, value)
        return self

    def each(self, f):
        for i, el in enumerate(self.elements):
            node = Node(el, self.document)
            result = f.invoke(node, (i, node)) if isinstance(f, Fn) else f(i, node)
            if result is False:
                break
        return self

    def parent(self):
        return Query(
            list(
                dict.fromkeys(
                    el.getparent() for el in self.elements if el.getparent() is not None
                )
            ),
            self.document,
        )

    def parents(self, selector=U):
        found = []
        for el in self.elements:
            for p in el.iterancestors():
                if (
                    selector is U or p in select(p, string(selector), True)
                ) and p not in found:
                    found.append(p)
        return Query(found, self.document)

    def attr(self, key, value=U):
        key = string(key)

        def attr_key(el):
            if ":" in key:
                prefix, name = key.split(":", 1)
                if prefix in el.nsmap:
                    return "{" + el.nsmap[prefix] + "}" + name
            return key

        if value is U:
            return (
                self.elements[0].get(attr_key(self.elements[0]), U)
                if self.elements
                else U
            )
        for el in self.elements:
            el.set(attr_key(el), string(value))
        return self

    def prop(self, key, value=U):
        key = string(key)
        if value is U:
            if not self.elements:
                return U
            if key in ("checked", "disabled", "selected"):
                return key in self.elements[0].attrib
            return self.attr(key)
        for el in self.elements:
            if key in ("checked", "disabled", "selected"):
                if truth(value):
                    el.set(key, key)
                else:
                    el.attrib.pop(key, None)
            else:
                el.set(key, string(value))
        return self

    def val(self, value=U):
        if value is U:
            if not self.elements:
                return U
            el = self.elements[0]
            if el.tag == "select":
                options = el.xpath(".//option")
                selected = next(
                    (x for x in options if "selected" in x.attrib),
                    options[0] if options else None,
                )
                return (
                    selected.get("value", "".join(selected.itertext()))
                    if selected is not None
                    else None
                )
            return el.get("value", "")
        for el in self.elements:
            if el.tag == "select":
                for option in el.xpath(".//option"):
                    if option.get("value", "".join(option.itertext())) == string(value):
                        option.set("selected", "selected")
                    else:
                        option.attrib.pop("selected", None)
            else:
                el.set("value", string(value))
        return self

    def append(self, value):
        for el in self.elements:
            if isinstance(value, Node):
                el.append(value.element)
                continue
            fragment = html.fragment_fromstring(string(value), create_parent="div")
            if fragment.text:
                if len(el):
                    el[-1].tail = (el[-1].tail or "") + fragment.text
                else:
                    el.text = (el.text or "") + fragment.text
            for child in list(fragment):
                el.append(child)
        return self

    def empty(self):
        for el in self.elements:
            for c in list(el):
                el.remove(c)
            el.text = None
        return self

    def show(self):
        return self

    def hide(self):
        return self

    def click(self, *args):
        return self

    def change(self, *args):
        return self

    def keyup(self, *args):
        return self

    def is_(self, selector):
        return bool(self.elements)

    def next(self):
        return Query(
            [e.getnext() for e in self.elements if e.getnext() is not None],
            self.document,
        )


class Document:
    def __init__(self, source):
        self.root = html.fromstring(source)
        for el in self.root.xpath("//script"):
            el.getparent().remove(el)

    def getElementById(self, id):
        nodes = self.root.xpath("//*[@id=$id]", id=string(id))
        return Node(nodes[0], self) if nodes else None

    def getElementsByName(self, name):
        return Array(
            Node(el, self)
            for el in self.root.xpath("//*[@name=$name]", name=string(name))
        )

    def query(self, value):
        if isinstance(value, Query):
            return value
        if isinstance(value, Node):
            return Query([value.element], self)
        if isinstance(value, etree._ElementTree):
            return Query([value.getroot()], self, True)
        if isinstance(value, etree._Element):
            return Query([value], self)
        if value is None or value is U:
            return Query([], self)
        if isinstance(value, str):
            return Query(select(self.root, value, True), self)
        raise TypeError(f"Unsupported query input {type(value).__name__}")

    def install(self, environment):
        def option(label, value):
            element = etree.Element("option", value=string(value))
            element.text = string(label)
            return Node(element, self)

        environment.local["Option"] = option
        environment.local.update(
            {
                "$": self.query,
                "document": self,
                "window": Obj(
                    location=Obj(protocol="https:", host="localhost", pathname="/")
                ),
                "overrideSaveData": lambda *args: False,
                "createPlayerList": lambda *args: U,
                "initializeHandlers": lambda *args: U,
            }
        )
