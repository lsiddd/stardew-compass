"""Executable layer boundaries, including when tests target the installed wheel."""

import ast
from importlib.resources import files


def sources(folder):
    for entry in folder.iterdir():
        if entry.is_dir():
            yield from sources(entry)
        elif entry.name.endswith(".py"):
            yield entry


def test_domain_has_no_infrastructure_or_presentation_dependencies():
    forbidden = (
        "stardew.infrastructure",
        "stardew.presentation",
        "stardew.application",
        "stardew.cli",
        "lxml",
        "PIL",
        "argparse",
    )
    for source in sources(files("stardew.domain")):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            imports = (
                [node.module or ""]
                if isinstance(node, ast.ImportFrom)
                else [name.name for name in node.names]
                if isinstance(node, ast.Import)
                else []
            )
            assert not any(name.startswith(forbidden) for name in imports), str(source)


def test_application_does_not_render_or_write_outputs():
    for source in sources(files("stardew.application")):
        for node in ast.walk(ast.parse(source.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ImportFrom):
                assert not (node.module or "").startswith(
                    ("stardew.infrastructure", "stardew.presentation", "stardew.cli")
                ), str(source)
