"""Installed-package imports and resource access outside the checkout."""

from importlib import resources
import json
from pathlib import Path
import subprocess
import sys
import tomllib

from stardew.infrastructure.game_data import load_game_data
from stardew.resources import data_path


def test_required_resource_assets_and_external_table_boundary():
    assert resources.files("stardew").joinpath("py.typed").is_file()
    assert (
        json.loads(data_path("maps.json").read_text(encoding="utf-8"))["Mountain"][
            "width"
        ]
        > 0
    )
    assert json.loads(data_path("maps.provenance.json").read_text(encoding="utf-8"))
    assert (
        data_path("fonts")
        .joinpath("DejaVuSans.ttf")
        .read_bytes()
        .startswith(b"\x00\x01\x00\x00")
    )
    assert data_path("fonts").joinpath("LICENSE.txt").is_file()
    schemas = resources.files("stardew.infrastructure.xnb").joinpath("schemas.json")
    assert json.loads(schemas.read_text(encoding="utf-8"))
    assert load_game_data().artifact_tables == {}
    assert not data_path("game").is_dir()


def test_bundled_catalogs_and_maps_are_reused_and_immutable():
    first, second = load_game_data(), load_game_data()
    assert first.maps is second.maps and first.catalogs is second.catalogs
    from dataclasses import FrozenInstanceError
    import pytest

    with pytest.raises(TypeError):
        first.maps["Mountain"] = None
    with pytest.raises(FrozenInstanceError):
        first.maps["Mountain"].width = 0
    with pytest.raises(TypeError):
        first.maps["Mountain"].layers["Back"]["width"] = 0


def test_one_entrypoint_and_required_runtime_dependencies():
    root = Path(__file__).parents[2]
    config = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    assert config["project"]["scripts"] == {"stardew": "stardew.cli:main"}
    dependencies = config["project"]["dependencies"]
    assert any(value.startswith("lxml") for value in dependencies)
    assert any(value.startswith("xxhash") for value in dependencies)
    assert not any(
        value.startswith(("cssselect", "html5lib", "Pillow")) for value in dependencies
    )
    assert any(
        value.startswith("Pillow")
        for value in config["project"]["optional-dependencies"]["plot"]
    )


def test_installed_entrypoint_and_resources_from_an_unrelated_directory(tmp_path):
    # Isolated mode excludes the checkout and PYTHONPATH. Editable or wheel
    # installation must expose the package and resource lookup through site-packages.
    command = [sys.executable, "-I", "-m", "stardew", "--version"]
    version = subprocess.run(command, cwd=tmp_path, text=True, capture_output=True)
    assert version.returncode == 0, version.stderr
    program = """from stardew.api import load_game_data
from stardew.resources import data_path
from stardew.infrastructure.xnb.reader import SCHEMAS
assert load_game_data().maps['Mountain'].width > 0
assert data_path('fonts').joinpath('DejaVuSans.ttf').read_bytes()
assert SCHEMAS
"""
    result = subprocess.run(
        [sys.executable, "-I", "-c", program],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr


def test_distributed_catalogs_have_no_presentation_markup():
    text = data_path("catalogs").joinpath("rules.json").read_text(encoding="utf-8")
    assert "<br" not in text and "<span" not in text


def test_outfit_catalog_preserves_pools_and_named_clothing_colors():
    pools = load_game_data().catalogs["predictor_makeover_choices"]
    assert {gender: len(pool) for gender, pool in pools.items()} == {
        "Male": 47,
        "Female": 48,
    }
    for pool in pools.values():
        for outfit in pool:
            assert {"hat", "shirt", "pants", "colors"} <= set(outfit)
            assert set(outfit["colors"]) <= {"hat", "shirt", "pants"}
    assert pools["Female"][0]["pants"] == "Tight Pants"
    assert pools["Female"][0]["colors"]["pants"] == "#dfd5b7"
    assert any(outfit["hat"] is None for outfit in pools["Female"])
    assert any(
        outfit.get("item_ids", {}).get("shirt") == "(S)1089"
        for outfit in pools["Female"]
    )
