"""The seeded System.Random algorithm and explicit C# numeric operations."""

import math
import struct

import xxhash

MAX = 2147483647
MASK = 0xFFFFFFFF
_SEED_INDICES = tuple(21 * i % 55 for i in range(1, 55))
_MIX_INDICES = tuple((i, 1 + (i + 30) % 55) for i in range(1, 56))


def i32(value):
    return (value + 2**31) % 2**32 - 2**31


def div(a, b):
    return (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1)


def rem(a, b):
    return a - div(a, b) * b


def f32(value):
    return struct.unpack("<f", struct.pack("<f", value))[0]


class SystemRandom:
    def __init__(self, seed):
        seed = int32(seed)
        subtraction = MAX if seed == -(2**31) else abs(seed)
        mj = 161803398 - subtraction
        values = self.values = [0] * 56
        values[55] = mj
        mk = 1
        for ii in _SEED_INDICES:
            values[ii] = mk
            # Both terms fit the signed range here, including the first seed.
            mk = mj - mk
            if mk < 0:
                mk += MAX
            mj = values[ii]
        for _ in range(4):
            for i, partner in _MIX_INDICES:
                value = values[i] - values[partner]
                # The initially negative slot 55 can overflow on the first
                # pass. Preserve unchecked Int32 subtraction before correction.
                if value > MAX:
                    value -= 4294967296
                elif value < -2147483648:
                    value += 4294967296
                if value < 0:
                    value += MAX
                values[i] = value
        self.index, self.partner = 0, 21

    def sample(self):
        self.index = self.index + 1 if self.index < 55 else 1
        self.partner = self.partner + 1 if self.partner < 55 else 1
        value = self.values[self.index] - self.values[self.partner]
        if value == MAX:
            value -= 1
        if value < 0:
            value += MAX
        self.values[self.index] = value
        return value

    def double(self):
        return self.sample() * (1.0 / MAX)

    def next(self, low=None, high=None):
        if low is None:
            return self.sample()
        if high is None:
            if low < 0:
                raise ValueError("Maximum must be nonnegative.")
            return int(self.double() * low)
        if low > high:
            raise ValueError("Minimum exceeds maximum.")
        width = high - low
        if width <= MAX:
            return int(self.double() * width) + low
        value = self.sample()
        if self.sample() % 2 == 0:
            value = -value
        return int(((value + MAX - 1) / (2 * MAX - 1)) * width) + low


# Share the seeded generator and Utility.CreateRandom double coercion.
# Integer division occurs at call sites before values enter the double API.
Random = SystemRandom
CSRandom = SystemRandom
trunc_div = div
trunc_rem = rem


def xxhash32(data: bytes) -> int:
    return xxhash.xxh32(data).intdigest()


def int32(value: int | float) -> int:
    """Report numeric coercion truncates finite fractions before wrapping."""
    if isinstance(value, int):
        return i32(value)
    return i32(math.trunc(value)) if math.isfinite(value) else 0


def hash_string(value: str) -> int:
    return i32(xxhash32(value.encode("utf-8")))


def hash_array(*values: int | float) -> int:
    return i32(
        xxhash32(struct.pack("<" + "i" * len(values), *(int32(v) for v in values)))
    )


def random_seed(*values: int | float, legacy: bool = False) -> int:
    """Utility.CreateRandomSeed: convert operands to double before remainder."""
    if len(values) > 5:
        raise ValueError("A random seed accepts at most five components.")
    parts = [math.fmod(v, MAX) for v in values] + [0] * (5 - len(values))
    if legacy:
        # C# adds left-to-right; Python 3.12+ sum compensates floating error.
        total = parts[0]
        for part in parts[1:]:
            total += part
        return math.trunc(math.fmod(total, MAX))
    return hash_array(*parts)


def create_seed(*values: int, legacy: bool = False) -> int:
    """Compatibility alias for the game's double-parameter seed method."""
    return random_seed(*values, legacy=legacy)


def for_day(state, a: int, b: int, c: int = 0) -> SystemRandom:
    metadata = getattr(state, "metadata", state)
    parts = (
        metadata.days_played,
        div(metadata.game_id, 2),
        i32(a),
        i32(b),
        i32(c),
    )
    seed = random_seed(*parts, legacy=bool(metadata.use_legacy_random))
    return SystemRandom(seed)
