import json
from pathlib import Path
import pytest
from PIL import Image
from types import SimpleNamespace
from stardew.domain.predictions.bubbles import BubbleEvent
from stardew.domain.predictions.artifacts import ArtifactResult, DigItem
from stardew.presentation.maps import (
    MapRenderer,
    rows_for_results,
    save_plots,
    draw_figure,
)


def test_group_repeated_coordinates_without_losing_events():
    events = [
        BubbleEvent("Town", 1, 2, 610, 800, "Bubbles"),
        BubbleEvent("Town", 1, 2, 900, None, "Frenzy"),
    ]
    rows = rows_for_results(events, "bubbles")
    assert len(rows) == 1 and len(rows[0][2]) == 2
    assert "06:10" in rows[0][2][0] and ">25:50" in rows[0][2][1]
    assert "Frenzy" in rows[0][2][1]


def test_save_png_coordinates_and_unicode(tmp_path, monkeypatch):
    save = SimpleNamespace(
        game_id=1,
        days_played=20,
        season="summer",
        day=20,
        year=1,
        game_version="1.6.15",
        use_legacy_random=False,
        times_fished=0,
        farm_type=0,
    )
    (tmp_path / "game/Content/Maps").mkdir(parents=True)
    background = Image.new("RGBA", (240, 240), "green")
    monkeypatch.setattr(
        MapRenderer, "render", lambda self, location: (background, 12, 20, 20)
    )
    results = [
        ArtifactResult("Town", 3, 4, (DigItem("(O)330", "Argila e relíquia", 2),), None)
    ]
    paths = save_plots(save, results, tmp_path / "out", tmp_path / "game", "artifacts")
    assert paths == [tmp_path / "out/artifacts_Town_day-20.png"]
    with Image.open(paths[0]) as image:
        assert image.format == "PNG"
        assert image.width >= 1100 and image.height >= 450
        # Ring location includes the tile-center offset, not a swapped X/Y.
        px, py = 32 + int(3.5 * 12), 108 + int(4.5 * 12)
        assert image.getpixel((px + 8, py)) == (255, 199, 107)
        assert image.getpixel((32 + int(4.5 * 12), 108 + int(3.5 * 12))) == (0, 128, 0)


def test_plot_errors_do_not_create_outputs(tmp_path, monkeypatch):
    save = SimpleNamespace(
        game_id=1,
        days_played=1,
        season="spring",
        day=1,
        year=1,
        game_version="1.6.15",
        use_legacy_random=False,
        times_fished=0,
        farm_type=0,
    )
    game = tmp_path / "game"
    (game / "Content/Maps").mkdir(parents=True)
    with pytest.raises(ValueError, match="outside"):
        save_plots(save, [], game / "out", game, "bubbles")
    with pytest.raises(ValueError, match="No installed map"):
        save_plots(
            save,
            [BubbleEvent("Town", 1, 2, 610, None, "Bubbles")],
            tmp_path / "out",
            game,
            "bubbles",
        )
    assert not (tmp_path / "out").exists()
    monkeypatch.setattr(
        MapRenderer,
        "render",
        lambda self, location: (Image.new("RGBA", (24, 24)), 12, 2, 2),
    )
    with pytest.raises(ValueError, match="outside installed map"):
        save_plots(
            save,
            [BubbleEvent("Town", 9, 9, 610, None, "Bubbles")],
            tmp_path / "out",
            game,
            "bubbles",
        )
    assert not (tmp_path / "out").exists()


def test_texture_season_and_island_handling(tmp_path, monkeypatch):
    maps = tmp_path / "Content/Maps"
    maps.mkdir(parents=True)
    for name in ("spring_test", "winter_test"):
        (maps / (name + ".xnb")).touch()
    calls = []
    monkeypatch.setattr(
        "stardew.presentation.maps.read_texture", lambda p: calls.append(p.name) or p
    )
    renderer = MapRenderer(tmp_path, "winter", 0)
    renderer.texture("spring_test", False)
    renderer.texture("spring_test", True)
    assert calls == ["winter_test.xnb", "spring_test.xnb"]
    with pytest.raises(ValueError, match="Invalid texture"):
        renderer.texture("../escape", False)


def test_plot_refuses_symlink_without_replacing_prior_files(tmp_path, monkeypatch):
    save = SimpleNamespace(days_played=20, season="summer", day=20, year=1, farm_type=0)
    game, out = tmp_path / "game", tmp_path / "out"
    (game / "Content/Maps").mkdir(parents=True)
    out.mkdir()
    background = Image.new("RGBA", (240, 240), "green")
    monkeypatch.setattr(
        MapRenderer, "render", lambda self, location: (background, 12, 20, 20)
    )
    prior = out / "bubbles_Town_day-20.png"
    prior.write_bytes(b"previous")
    protected = tmp_path / "protected.png"
    protected.write_bytes(b"personal")
    (out / "bubbles_Forest_day-20.png").symlink_to(protected)
    results = [
        BubbleEvent("Town", 1, 2, 610, None, "Bubbles"),
        BubbleEvent("Forest", 1, 2, 610, None, "Bubbles"),
    ]
    with pytest.raises(ValueError, match="symbolic link"):
        save_plots(save, results, out, game, "bubbles")
    assert prior.read_bytes() == b"previous"
    assert protected.read_bytes() == b"personal"


@pytest.mark.parametrize("connection", ["same_path", "hardlink", "symlink"])
def test_game_state_input_save_is_protected_from_png_outputs(
    tmp_path, monkeypatch, connection
):
    import os
    from stardew.infrastructure.saves import SaveError

    metadata = SimpleNamespace(
        days_played=20, season="summer", day=20, year=1, farm_type=0
    )
    game, out = tmp_path / "game", tmp_path / "out"
    (game / "Content/Maps").mkdir(parents=True)
    out.mkdir()
    target = out / "bubbles_Forest_day-20.png"
    source = target if connection == "same_path" else tmp_path / "input-save.xml"
    original = b"<SaveGame>personal saved state</SaveGame>"
    source.write_bytes(original)
    if connection == "hardlink":
        os.link(source, target)
    elif connection == "symlink":
        target.symlink_to(source)
    prior = out / "bubbles_Town_day-20.png"
    prior.write_bytes(b"previous figure")
    state = SimpleNamespace(metadata=metadata, source=source)
    background = Image.new("RGBA", (240, 240), "green")
    monkeypatch.setattr(
        MapRenderer, "render", lambda self, location: (background, 12, 20, 20)
    )
    results = [
        BubbleEvent("Town", 1, 2, 610, None, "Bubbles"),
        BubbleEvent("Forest", 1, 2, 610, None, "Bubbles"),
    ]
    with pytest.raises(SaveError, match="overwrite the input save"):
        save_plots(state, results, out, game, "bubbles")
    assert source.read_bytes() == original
    assert target.read_bytes() == original
    assert prior.read_bytes() == b"previous figure"
    assert not list(out.glob(".*"))
