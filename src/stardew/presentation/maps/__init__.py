"""Save annotated PNG maps using local game graphics and optional Pillow."""

from collections import OrderedDict
from io import BytesIO
from ...resources import data_path
from pathlib import Path
import re

from ...infrastructure.files import atomic_write_many
from ...infrastructure.saves.output import check_output_path
from ...infrastructure.xnb.graphics import read_texture, read_visual_map

MAP_NAMES = {
    "IslandNorth": "Island_N",
    "IslandSouth": "Island_S",
    "IslandSouthEast": "Island_SE",
    "IslandWest": "Island_W",
    "DesertFestival": "Desert-Festival",
}
FARM_MAPS = [
    "Farm",
    "Farm_Fishing",
    "Farm_Foraging",
    "Farm_Mining",
    "Farm_Combat",
    "Farm_FourCorners",
    "Farm_Island",
    "Farm_Ranching",
]
SEASONS = {
    "spring": "Spring",
    "summer": "Summer",
    "fall": "Fall",
    "winter": "Winter",
}


def pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise ValueError(
            "Plotting requires Pillow. Run: uv sync --extra plot"
        ) from error
    return Image, ImageDraw, ImageFont


class MapRenderer:
    def __init__(self, game_directory, season, farm_type):
        self.content = Path(game_directory).expanduser().resolve() / "Content"
        if not (self.content / "Maps").is_dir():
            raise ValueError(f"Game maps directory not found: {self.content / 'Maps'}")
        self.season, self.farm_type = season, farm_type
        self.textures = {}

    def texture(self, source, tropical):
        path = Path(source.replace("\\", "/"))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Invalid texture path: {source}")
        if path.parts and path.parts[0] != "Maps":
            path = Path("Maps") / path
        if path.suffix.lower() != ".xnb":
            path = path.with_suffix(".xnb")
        # Island sheets remain tropical; mainland sheets follow the saved season.
        if not tropical and path.name.startswith(
            ("spring_", "summer_", "fall_", "winter_")
        ):
            seasonal = path.with_name(self.season + "_" + path.name.split("_", 1)[1])
            if (self.content / seasonal).is_file():
                path = seasonal
        if path not in self.textures:
            self.textures[path] = read_texture(self.content / path)
        return self.textures[path]

    def render(self, location):
        Image, _, _ = pillow()
        name = MAP_NAMES.get(location, location)
        if location == "Farm":
            if not 0 <= self.farm_type < len(FARM_MAPS):
                raise ValueError("Unsupported farm type for plotting.")
            name = FARM_MAPS[self.farm_type]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
            raise ValueError(f"Unsupported map location: {location}")
        source = self.content / "Maps" / (name + ".xnb")
        if not source.is_file():
            raise ValueError(f"No installed map for {location}: {source}")
        visual = read_visual_map(source)
        pixels = max(4, min(12, 1080 // visual.width))
        canvas = Image.new(
            "RGBA", (visual.width * pixels, visual.height * pixels), "#182630"
        )
        tiles = {}
        for layer in visual.layers:
            if not layer.visible or layer.name.lower().startswith("paths"):
                continue
            for position, tile in enumerate(layer.tiles):
                if tile is None:
                    continue
                if tile not in tiles:
                    sheet_id, index = tile
                    sheet = visual.sheets[sheet_id]
                    texture = self.texture(sheet.source, location.startswith("Island"))
                    x = sheet.margin[0] + index % sheet.columns * (
                        sheet.tile_width + sheet.spacing[0]
                    )
                    y = sheet.margin[1] + index // sheet.columns * (
                        sheet.tile_height + sheet.spacing[1]
                    )
                    if (
                        x < 0
                        or y < 0
                        or x + sheet.tile_width > texture.width
                        or y + sheet.tile_height > texture.height
                    ):
                        raise ValueError(
                            f"Tile outside texture: {sheet.source}, index {index}"
                        )
                    tiles[tile] = texture.crop(
                        (x, y, x + sheet.tile_width, y + sheet.tile_height)
                    ).resize((pixels, pixels), Image.Resampling.NEAREST)
                x, y = position % layer.width, position // layer.width
                canvas.alpha_composite(tiles[tile], (x * pixels, y * pixels))
        return canvas, pixels, visual.width, visual.height


def clock(time):
    return f"{time // 100:02}:{time % 100:02}"


def rows_for_results(results, mode):
    """A shared marker for repeated coordinates; retain every event/drop."""
    grouped = OrderedDict()
    for result in results:
        key = result.x, result.y
        entries = grouped.setdefault(key, [])
        if mode == "bubbles":
            end = clock(result.end) if result.end is not None else ">25:50"
            entries.append(
                f"{clock(result.start)} – {end}"
                + (" / Frenzy" if result.kind == "Frenzy" else "")
            )
        else:
            entries.append(
                " + ".join(f"{item.quantity}× {item.name}" for item in result.items)
                or "No items"
            )
            if result.note:
                entries.append(result.note)
    return [(x, y, entries) for (x, y), entries in grouped.items()]


def wrap(draw, text, font, width):
    lines, current = [], ""
    for character in text:
        candidate = current + character
        if current and draw.textlength(candidate, font=font) > width:
            split = current.rfind(" ")
            if split > 0:
                lines.append(current[:split])
                current = current[split + 1 :] + character
            else:
                lines.append(current)
                current = character
        else:
            current = candidate
    return lines + ([current] if current else [])


def draw_figure(background, pixels, rows, save, location, mode):
    Image, ImageDraw, ImageFont = pillow()
    font_data = data_path("fonts").joinpath("DejaVuSans.ttf").read_bytes()
    font, small, title_font = (
        ImageFont.truetype(BytesIO(font_data), size=s) for s in (19, 16, 29)
    )
    measure = ImageDraw.Draw(background)
    legend_width, margin, header, footer = 500, 32, 108, 102
    blocks = []
    for x, y, entries in rows:
        lines = [
            line
            for entry in entries
            for line in wrap(measure, entry, font, legend_width - 70)
        ]
        blocks.append((x, y, lines))
    legend_height = 60 + sum(45 + len(lines) * 26 for _, _, lines in blocks)
    map_width = max(560, background.width)
    width = margin * 3 + map_width + legend_width
    height = header + max(background.height, legend_height) + footer
    image = Image.new("RGB", (width, height), "#101c27")
    image.paste(background.convert("RGB"), (margin, header))
    draw = ImageDraw.Draw(image)
    accent = "#5ee7ed" if mode == "bubbles" else "#ffc76b"
    label = "Fishing bubbles" if mode == "bubbles" else "Artifact spots"
    draw.text((margin, 20), f"{location}  /  {label}", font=title_font, fill="#f5f5ee")
    date = f"{SEASONS.get(save.season, save.season)} {save.day} · Year {save.year} · Day {save.days_played}"
    draw.text((margin, 61), date, font=font, fill="#b5c4ce")
    lx, ly = map_width + margin * 2, header
    draw.text((lx, ly), "MAP MARKERS", font=font, fill=accent)
    ly += 46
    for number, (x, y, lines) in enumerate(blocks, 1):
        px, py = margin + (x + 0.5) * pixels, header + (y + 0.5) * pixels
        # Contrast halo keeps markers visible over both sand and water.
        draw.ellipse(
            (px - 14, py - 14, px + 14, py + 14),
            fill="#101c27",
            outline="#ffffff",
            width=2,
        )
        draw.ellipse((px - 10, py - 10, px + 10, py + 10), fill=accent)
        draw.text((px, py), str(number), font=small, fill="#101c27", anchor="mm")
        draw.text((lx, ly), f"{number:02}   ({x}, {y})", font=font, fill=accent)
        ly += 28
        for line in lines:
            draw.text((lx + 4, ly), line, font=font, fill="#e5e8eb")
            ly += 26
        ly += 17
    # Coordinate ticks locate the tile origin without covering the art with a grid.
    for x in range(0, background.width // pixels, 10):
        draw.text(
            (margin + (x + 0.5) * pixels, header - 18),
            str(x),
            font=small,
            fill="#93a9b8",
            anchor="mm",
        )
    for y in range(0, background.height // pixels, 10):
        draw.text(
            (margin - 5, header + (y + 0.5) * pixels),
            str(y),
            font=small,
            fill="#93a9b8",
            anchor="rm",
        )
    notes = [
        "Coordinates start at zero. X → right; Y → down. Island and festival access is not filtered.",
        "Static map: saved buildings, objects and changes made during the session are not shown.",
    ]
    if mode == "bubbles":
        notes.append(
            ">25:50 = bubbles still active at the last simulated time; end times are exclusive."
        )
    else:
        notes.append(
            "Each spot is evaluated independently; a digging route is not simulated."
        )
    for i, note in enumerate(notes):
        draw.text(
            (margin, height - footer + 18 + i * 24), note, font=small, fill="#b5c4ce"
        )
    return image


def save_plots(save, results, output_directory, game_directory, mode):
    source = getattr(save, "source", None)
    save = getattr(save, "metadata", save)
    pillow()
    if mode not in ("bubbles", "artifacts"):
        raise ValueError(f"Unknown plot mode: {mode}")
    output = Path(output_directory).expanduser().resolve()
    game = Path(game_directory).expanduser().resolve()
    if output == game or game in output.parents:
        raise ValueError("Plot output must be outside the game installation.")
    renderer = MapRenderer(game, save.season, save.farm_type)
    locations = OrderedDict()
    for result in results:
        locations.setdefault(result.location, []).append(result)
    prepared = []
    for location, local_results in locations.items():
        background, pixels, width, height = renderer.render(location)
        rows = rows_for_results(local_results, mode)
        if any(not (0 <= x < width and 0 <= y < height) for x, y, _ in rows):
            raise ValueError(
                f"Prediction coordinates outside installed map: {location}"
            )
        image = draw_figure(background, pixels, rows, save, location, mode)
        safe = re.sub(r"[^A-Za-z0-9_-]", "_", location)
        path = output / f"{mode}_{safe}_day-{save.days_played}.png"
        if source is not None:
            check_output_path(path, source)
        prepared.append((path, image))
    # All maps/textures are validated before creating the output directory.
    encoded = {}
    for path, image in prepared:
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        encoded[path] = buffer.getvalue()
    atomic_write_many(encoded)
    return [path for path, _ in prepared]
