"""Small value-semantics layer for the translated, statically compiled rules.

No JavaScript engine or eval is used. This module makes coercions explicit so
ports preserve upstream behavior (notably integer keys, +, and remainder).
"""

from __future__ import annotations
import functools
import math
import re


class Undefined:
    def __repr__(self):
        return "undefined"


U = Undefined()


class Obj(dict):
    pass


class Array(list):
    def __init__(self, values=()):
        super().__init__(values)
        self.properties = {}


class Env:
    def __init__(self, parent=None):
        self.local = {}
        self.parent = parent

    def __getitem__(self, key):
        if key in self.local:
            return self.local[key]
        return self.parent[key] if self.parent is not None else U

    def declare(self, names):
        self.local.update(dict.fromkeys(names, U))

    def set(self, key, value):
        if key in self.local or self.parent is None:
            self.local[key] = value
        else:
            self.parent.set(key, value)
        return value


class Fn:
    def __init__(self, function, environment):
        self.function = function
        self.environment = environment

    def __call__(self, *args):
        return self.invoke(U, args)

    def invoke(self, this, args):
        return self.function(self.environment, this, args)


def call(f, *args):
    if not callable(f):
        raise TypeError(f"Rule tried to call {f!r}")
    return f(*args)


def wrap(value):
    if isinstance(value, dict):
        return Obj({str(k): wrap(v) for k, v in value.items()})
    if isinstance(value, list):
        return Array(wrap(v) for v in value)
    return value


def truth(v):
    if v is U or v is None:
        return False
    if isinstance(v, (list, dict)):
        return True
    if isinstance(v, float) and math.isnan(v):
        return False
    return bool(v)


def string(v):
    if v is U:
        return "undefined"
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, str):
        return v
    if isinstance(v, float):
        if math.isnan(v):
            return "NaN"
        if math.isinf(v):
            return "Infinity" if v > 0 else "-Infinity"
        if v.is_integer():
            return str(int(v))
        return str(v)
    if isinstance(v, list):
        return ",".join("" if x is U or x is None else string(x) for x in v)
    if isinstance(v, dict):
        return "[object Object]"
    return str(v)


def number(v=U):
    if v is U:
        return math.nan
    if v is None:
        return 0
    if isinstance(v, (int, float)):
        return v
    s = string(v).strip()
    if not s:
        return 0
    try:
        return int(s, 16) if s.lower().startswith(("0x", "-0x")) else float(s)
    except ValueError:
        return math.nan


def integer(v=0):
    n = number(v)
    return math.trunc(n) if math.isfinite(n) else 0


def int32(v):
    return ((integer(v) + 2**31) % 2**32) - 2**31


def parse_int(v, base=10):
    s = string(v).lstrip()
    pattern = r"^[+-]?[0-9]+" if base == 10 else r"^[+-]?(?:0[xX])?[0-9a-fA-F]+"
    m = re.match(pattern, s)
    try:
        return int(m[0], integer(base)) if m else math.nan
    except ValueError:
        return math.nan


def strict_equal(a, b):
    if a is U or b is U or a is None or b is None:
        return a is b
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, (dict, list)):
        return a is b
    return a == b


def binary(op, a, b):
    if op == "+":
        if isinstance(a, (dict, list)):
            a = string(a)
        if isinstance(b, (dict, list)):
            b = string(b)
        return (
            string(a) + string(b)
            if isinstance(a, str) or isinstance(b, str)
            else number(a) + number(b)
        )
    if op in ("===", "!=="):
        return strict_equal(a, b) if op == "===" else not strict_equal(a, b)
    if op in ("==", "!="):
        equal = (a is None and b is U) or (a is U and b is None) or strict_equal(a, b)
        if not equal and a is not U and b is not U and a is not None and b is not None:
            if isinstance(a, (str, int, float, bool)) and isinstance(
                b, (str, int, float, bool)
            ):
                equal = number(a) == number(b)
        return equal if op == "==" else not equal
    if op == "in":
        return string(a) in keys(b)
    if op == "^":
        return int32(a) ^ int32(b)
    if op in ("<", ">", "<=", ">="):
        if not (isinstance(a, str) and isinstance(b, str)):
            a, b = number(a), number(b)
        if op == "<":
            return a < b
        if op == ">":
            return a > b
        if op == "<=":
            return a <= b
        return a >= b
    a, b = number(a), number(b)
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        return a / b if b else (math.nan if not a else math.copysign(math.inf, a))
    if op == "%":
        return math.fmod(a, b) if b else math.nan
    raise ValueError(op)


def unary(op, v):
    if op == "!":
        return not truth(v)
    if op == "-":
        return -number(v)
    if op == "+":
        return number(v)
    if op == "typeof":
        if v is U:
            return "undefined"
        if isinstance(v, bool):
            return "boolean"
        if isinstance(v, (int, float)):
            return "number"
        if isinstance(v, str):
            return "string"
        if callable(v):
            return "function"
        return "object"
    raise ValueError(op)


def keys(v):
    if isinstance(v, dict):
        numeric = sorted(
            (k for k in v if k.isdecimal() and str(int(k)) == k and int(k) < 2**32 - 1),
            key=int,
        )
        numeric_keys = set(numeric)
        return Array(numeric + [k for k in v if k not in numeric_keys])
    if isinstance(v, Array):
        return Array([*(str(i) for i in range(len(v)) if v[i] is not U), *v.properties])
    if isinstance(v, (list, str)):
        return Array(str(i) for i in range(len(v)))
    raise TypeError(f"Cannot enumerate {v!r}")


def get(v, key):
    k = string(key)
    if v is U or v is None:
        raise TypeError(f"Cannot read {k!r} from {v!r}")
    if isinstance(v, dict):
        if k in v:
            return v[k]
        if k == "hasOwnProperty":
            return lambda x: string(x) in v
        return U
    if isinstance(v, Array) and k in v.properties:
        return v.properties[k]
    if isinstance(v, (list, str)):
        if k == "length":
            return len(v)
        if re.fullmatch(r"0|[1-9][0-9]*", k):
            i = int(k)
            return v[i] if i < len(v) else U
        if k == "slice":
            return lambda a=0, b=U: type(v)(
                v[integer(a) : None if b is U else integer(b)]
            )
        if k == "indexOf":
            return lambda x: v.index(x) if x in v else -1
        if k == "includes":
            return lambda x: x in v
        if k == "hasOwnProperty":
            return lambda x: (
                (string(x) in v.properties if isinstance(v, Array) else False)
                or (
                    string(x).isdigit()
                    and int(string(x)) < len(v)
                    and v[int(string(x))] is not U
                )
            )
    if k == "toString":
        return lambda: string(v)
    if isinstance(v, str):
        methods = {
            "toLowerCase": v.lower,
            "toUpperCase": v.upper,
            "trim": v.strip,
            "split": lambda sep=U: (
                Array([v])
                if sep is U
                else (Array(v) if sep == "" else Array(v.split(string(sep))))
            ),
            "substring": lambda a, b=U: (
                v[min(max(0, integer(a)), len(v)) :]
                if b is U
                else v[
                    min(max(0, integer(a)), max(0, integer(b))) : max(
                        max(0, integer(a)), max(0, integer(b))
                    )
                ]
            ),
            "substr": lambda a, b=U: (
                v[integer(a) :]
                if b is U
                else v[integer(a) : integer(a) + max(0, integer(b))]
            ),
            "replace": lambda p, r: replace(v, p, r),
            "match": lambda p: match(v, p),
        }
        if k in methods:
            return methods[k]
    if isinstance(v, list):
        if k == "push":

            def push(*items):
                v.extend(items)
                return len(v)

            return push
        if k == "join":
            return lambda sep=",": string(sep).join(
                "" if x is None or x is U else string(x) for x in v
            )
        if k == "sort":

            def sort(compare=U):
                v.sort(
                    key=(lambda x: string(x))
                    if compare is U
                    else functools.cmp_to_key(lambda a, b: integer(call(compare, a, b)))
                )
                return v

            return sort
        if k == "splice":

            def splice(start, count=U, *items):
                i = integer(start)
                i = max(0, len(v) + i) if i < 0 else min(i, len(v))
                n = len(v) - i if count is U else max(0, integer(count))
                removed = Array(v[i : i + n])
                v[i : i + n] = items
                return removed

            return splice
        if k == "map":
            return lambda f: Array(call(f, x, i, v) for i, x in enumerate(v))
        if k == "forEach":

            def for_each(f):
                for i, x in enumerate(list(v)):
                    call(f, x, i, v)
                return U

            return for_each
    if isinstance(v, (int, float)) and k == "toFixed":
        return lambda n=0: format(v, f".{integer(n)}f")
    if hasattr(v, "js_get"):
        return v.js_get(k)
    return getattr(v, k, U)


def put(v, key, value):
    k = string(key)
    if isinstance(v, dict):
        v[k] = value
    elif isinstance(v, list):
        if k == "length":
            length = integer(value)
            del v[length:]
            v.extend([U] * max(0, length - len(v)))
        elif not re.fullmatch(r"0|[1-9][0-9]*", k):
            v.properties[k] = value
        else:
            i = integer(key)
            if i < 0:
                raise ValueError("Negative array property")
            v.extend([U] * max(0, i + 1 - len(v)))
            v[i] = value
    elif hasattr(v, "js_put"):
        v.js_put(k, value)
    else:
        setattr(v, k, value)
    return value


def delete(v, k):
    v.pop(string(k), None)
    return True


def update_env(e, key, delta, prefix):
    old = number(e[key])
    e.set(key, old + delta)
    return old + delta if prefix else old


def update_prop(v, key, delta, prefix):
    old = number(get(v, key))
    put(v, key, old + delta)
    return old + delta if prefix else old


class Regex:
    def __init__(self, pattern, flags=""):
        self.pattern = re.compile(pattern, re.I if "i" in flags else 0)
        self.global_ = "g" in flags

    def test(self, s):
        return self.pattern.search(string(s)) is not None


def replace(s, p, r):
    if isinstance(p, Regex):

        def sub(m):
            return re.sub(
                r"\$(\d+|&|\$)",
                lambda x: (
                    m[0]
                    if x[1] == "&"
                    else "$"
                    if x[1] == "$"
                    else (m[int(x[1])] or "")
                ),
                string(r),
            )

        return p.pattern.sub(sub, s, count=0 if p.global_ else 1)
    return s.replace(string(p), string(r), 1)


def match(s, p):
    if not isinstance(p, Regex):
        p = Regex(string(p))
    if p.global_:
        found = Array(m[0] for m in p.pattern.finditer(s))
        return found if found else None
    m = p.pattern.search(s)
    return Array([m[0], *m.groups()]) if m else None


class BigInt:
    def __init__(self, value):
        self.value = value.value if isinstance(value, BigInt) else int(value)

    def __str__(self):
        return str(self.value)

    def js_get(self, k):
        def val(x):
            return x.value if isinstance(x, BigInt) else int(x)

        ops = {
            "and": lambda x: BigInt(self.value & val(x)),
            "mod": lambda x: BigInt(
                self.value % val(x) if self.value >= 0 else -((-self.value) % val(x))
            ),
            "divide": lambda x: BigInt(
                (1 if self.value * val(x) >= 0 else -1)
                * (abs(self.value) // abs(val(x)))
            ),
            "times": lambda x: BigInt(self.value * val(x)),
            "plus": lambda x: BigInt(self.value + val(x)),
            "add": lambda x: BigInt(self.value + val(x)),
            "toJSNumber": lambda: self.value,
        }
        return ops.get(k, U)


def base_environment():
    e = Env()
    e.local.update(
        {
            "undefined": U,
            "NaN": math.nan,
            "Number": number,
            "String": string,
            "Boolean": truth,
            "parseInt": parse_int,
            "parseFloat": number,
            "isNaN": lambda x: math.isnan(number(x)),
            "bigInt": BigInt,
            "Math": Obj(
                floor=lambda x: math.floor(number(x)),
                ceil=lambda x: math.ceil(number(x)),
                abs=abs,
                min=min,
                max=max,
                round=lambda x: math.floor(number(x) + 0.5),
                imul=lambda a, b: int32(int32(a) * int32(b)),
            ),
            "Object": Obj(keys=keys),
            "console": Obj(log=lambda *args: U),
            "RegExp": Regex,
        }
    )
    return e
