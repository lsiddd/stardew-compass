"""XNB v5 readers with explicit Stardew Valley 1.6.15 schemas; no assemblies."""

import json
from importlib.resources import files
import math
import re
from pathlib import Path
import struct
from ...domain.numeric import f32, i32
from .lzx import decompress_frames

SCHEMAS = json.loads(
    files(__package__).joinpath("schemas.json").read_text(encoding="utf-8")
)
ENUMS = {
    "StardewValley.Season",
    "StardewValley.GameData.MusicContext",
    "StardewValley.GameData.QuantityModifier+ModificationType",
    "StardewValley.GameData.QuantityModifier+QuantityModifierMode",
}


def type_name(text):
    """Remove assembly identities, retaining nested generic type arguments."""
    if "[[" not in text:
        return text.split(",", 1)[0].strip()
    base, rest = text.split("[[", 1)
    args, start, depth = [], 0, 0
    for i, char in enumerate(rest):
        if char == "[":
            depth += 1
        elif char == "]":
            if depth:
                depth -= 1
            else:
                args.append(type_name(rest[start:i]))
                if rest[i + 1 : i + 2] == "]":
                    break
                start = i + 3
                # Skip the opening '[' of the next argument below.
        if i == start - 1 and char == "[":
            depth -= 1
    return base + "<" + "|".join(args) + ">"


def generic(name):
    if "<" not in name:
        return name, []
    base, rest = name.split("<", 1)
    args, start, depth = [], 0, 0
    for i, char in enumerate(rest[:-1]):
        if char == "<":
            depth += 1
        elif char == ">":
            depth -= 1
        elif char == "|" and depth == 0:
            args.append(rest[start:i])
            start = i + 1
    args.append(rest[start:-1])
    return base, args


PRIMITIVES = {
    "String": "System.String",
    "Int32": "System.Int32",
    "Boolean": "System.Boolean",
    "Single": "System.Single",
    "Double": "System.Double",
    "Point": "Microsoft.Xna.Framework.Point",
    "Rectangle": "Microsoft.Xna.Framework.Rectangle",
}
VALUES = set(PRIMITIVES.values()) - {"System.String"} | ENUMS


def reader_type(name):
    versions = re.findall(r"StardewValley\.GameData, Version=([0-9.]+)", name)
    if any(v != "1.6.15.24356" for v in versions):
        raise ValueError("Incompatible Stardew Valley XNB schema version.")
    prefix = "Microsoft.Xna.Framework.Content."
    if not name.startswith(prefix):
        raise ValueError(f"Unknown XNB reader: {name}")
    base, args = generic(type_name(name[len(prefix) :]))
    if base.endswith("Reader") and base[:-6] in PRIMITIVES and not args:
        return PRIMITIVES[base[:-6]]
    kinds = {
        "DictionaryReader`2": ("System.Collections.Generic.Dictionary`2", 2),
        "ListReader`1": ("System.Collections.Generic.List`1", 1),
        "NullableReader`1": ("System.Nullable`1", 1),
    }
    if base in kinds and len(args) == kinds[base][1]:
        return kinds[base][0] + "<" + "|".join(args) + ">"
    if base == "ReflectiveReader`1" and len(args) == 1 and args[0] in SCHEMAS:
        return args[0]
    if base == "EnumReader`1" and len(args) == 1 and args[0] in ENUMS:
        return args[0]
    raise ValueError(f"Unknown XNB reader or incompatible schema: {name}")


def float_json(value):
    """System.Text.Json writes the shortest decimal that roundtrips to Single."""
    if not math.isfinite(value):
        raise ValueError("Non-finite XNB numeric value.")
    for precision in range(1, 10):
        decimal = float(format(value, f".{precision}g"))
        try:
            if f32(decimal) == value:
                return decimal
        except OverflowError:
            continue
    return value


class Reader:
    def __init__(self, data):
        self.data, self.pos, self.readers = data, 0, []

    def take(self, count):
        if count < 0 or self.pos + count > len(self.data):
            raise ValueError(f"Truncated XNB at byte {self.pos}.")
        result = self.data[self.pos : self.pos + count]
        self.pos += count
        return result

    def unpack(self, fmt):
        return struct.unpack("<" + fmt, self.take(struct.calcsize("<" + fmt)))[0]

    def seven(self):
        value = 0
        for shift in range(0, 35, 7):
            byte = self.unpack("B")
            if shift == 28 and byte > 7:
                raise ValueError("Invalid XNB 7-bit integer.")
            value |= (byte & 127) << shift
            if byte < 128:
                return value
        raise ValueError("Invalid XNB 7-bit integer.")

    def string(self):
        return self.take(self.seven()).decode("utf-8")

    def count(self):
        count = self.unpack("i")
        if not 0 <= count <= len(self.data) - self.pos:
            raise ValueError("Invalid XNB collection count.")
        return count

    def object(self, expected=None):
        index = self.seven()
        if index == 0:
            return None
        if index > len(self.readers):
            raise ValueError("Unknown XNB reader index.")
        name = self.readers[index - 1]
        if expected is not None and name != expected:
            raise ValueError(f"Incompatible XNB type: expected {expected}, got {name}.")
        return self.raw(name)

    def value(self, name):
        return (
            self.raw(name)
            if name in VALUES or name.startswith("System.Nullable`1<")
            else self.object(name)
        )

    def raw(self, name):
        if name == "System.String":
            return self.string()
        if name == "System.Int32" or name in ENUMS:
            return self.unpack("i")
        if name == "System.Boolean":
            return self.unpack("B") != 0
        if name == "System.Single":
            return float_json(self.unpack("f"))
        if name == "System.Double":
            value = self.unpack("d")
            if not math.isfinite(value):
                raise ValueError("Non-finite XNB numeric value.")
            return value
        if name == "Microsoft.Xna.Framework.Point":
            x, y = self.unpack("i"), self.unpack("i")
            return {"X": x, "Y": y}
        if name == "Microsoft.Xna.Framework.Rectangle":
            x, y, w, h = [self.unpack("i") for _ in range(4)]
            return {
                "Left": x,
                "Right": i32(x + w),
                "Top": y,
                "Bottom": i32(y + h),
                "IsEmpty": x == y == w == h == 0,
                "Location": {"X": x, "Y": y},
                "Size": {"X": w, "Y": h},
                "Center": {"X": i32(x + int(w / 2)), "Y": i32(y + int(h / 2))},
                "X": x,
                "Y": y,
                "Width": w,
                "Height": h,
            }
        base, args = generic(name)
        if base == "System.Nullable`1":
            return self.raw(args[0]) if self.unpack("B") else None
        if base == "System.Collections.Generic.List`1":
            return [self.value(args[0]) for _ in range(self.count())]
        if base == "System.Collections.Generic.Dictionary`2":
            result = {}
            for _ in range(self.count()):
                key = self.value(args[0])
                value = self.value(args[1])
                if key is None or key in result:
                    raise ValueError("Null or duplicate XNB dictionary key.")
                result[key] = value
            return result
        if name in SCHEMAS:
            schema = SCHEMAS[name]
            inherited = self.raw(schema["base"]) if schema["base"] else {}
            own = {field: self.value(kind) for field, kind in schema["members"]}
            # JSON serializes derived properties before base properties.
            result = own | inherited
            if (
                name == "StardewValley.GameData.GenericSpawnItemData"
                and result["Id"] is None
            ):
                item = result["ItemId"]
                if item is None and result["RandomItemId"]:
                    item = "|".join(v or "" for v in result["RandomItemId"])
                result["Id"] = (
                    "???"
                    if item is None
                    else item + (" (Recipe)" if result["IsRecipe"] else "")
                )
            if (
                name == "StardewValley.GameData.Locations.LocationMusicData"
                and result["Id"] is None
            ):
                result["Id"] = result["Track"]
            return result
        raise ValueError(f"Unsupported XNB type: {name}")

    def read(self, expected=None):
        for _ in range(self.seven()):
            name = self.string()
            version = self.unpack("i")
            if version != 0:
                raise ValueError(f"Unsupported XNB reader version: {version}")
            self.readers.append(reader_type(name))
        if self.seven():
            raise ValueError("Shared XNB resources are unsupported for these tables.")
        result = self.object(expected)
        if self.pos != len(self.data):
            raise ValueError(
                f"Trailing XNB data: incompatible schema at byte {self.pos}."
            )
        return result


def unpack_xnb(data):
    r = Reader(data)
    if r.take(3) != b"XNB":
        raise ValueError("Invalid XNB signature.")
    if r.take(1) not in (b"w", b"m", b"x"):
        raise ValueError("Unsupported XNB platform.")
    if r.unpack("B") != 5:
        raise ValueError("Only XNB version 5 is supported.")
    flags = r.unpack("B")
    if flags & ~0x81:
        raise ValueError("Unsupported XNB compression or flags (LZ4 is not supported).")
    if r.unpack("I") != len(data):
        raise ValueError("XNB file length mismatch.")
    if flags & 0x80:
        size = r.unpack("I")
        return decompress_frames(data[r.pos :], size)
    return data[r.pos :]


def read_xnb(path):
    return Reader(unpack_xnb(Path(path).read_bytes())).read()
