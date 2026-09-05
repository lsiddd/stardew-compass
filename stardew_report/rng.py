"""Stardew's seeded System.Random and deterministic 1.6 seed helpers.

Adapted from MouseyPounds' MIT cs-random.js. Integer wrapping and negative
remainders are intentional; Python's default arithmetic differs here.
"""

import math
import struct
import xxhash
from .runtime import BigInt, U, get, int32, truth

MAX = 2147483647


class CSRandom:
    def __init__(self, seed):
        seed = int32(seed)
        subtraction = MAX if seed == -2147483648 else abs(seed)
        mj = 161803398 - subtraction
        self.values = [0] * 56
        self.values[55] = mj
        mk = 1
        for i in range(1, 55):
            ii = (21 * i) % 55
            self.values[ii] = mk
            mk = mj - mk
            if mk < 0:
                mk += MAX
            mj = self.values[ii]
        for _ in range(4):
            for i in range(1, 56):
                self.values[i] = int32(self.values[i] - self.values[1 + (i + 30) % 55])
                if self.values[i] < 0:
                    self.values[i] += MAX
        self.inext = 0
        self.inextp = 21

    def InternalSample(self):
        self.inext = self.inext + 1 if self.inext < 55 else 1
        self.inextp = self.inextp + 1 if self.inextp < 55 else 1
        value = self.values[self.inext] - self.values[self.inextp]
        if value == MAX:
            value -= 1
        if value < 0:
            value += MAX
        self.values[self.inext] = value
        return value

    def NextDouble(self):
        return self.InternalSample() * (1.0 / MAX)

    Sample = NextDouble

    def GetSampleForLargeRange(self):
        value = self.InternalSample()
        if self.InternalSample() % 2 == 0:
            value = -value
        return (value + MAX - 1) / (2 * MAX - 1)

    def Next(self, a=U, b=U):
        if a is U:
            return self.InternalSample()
        low, high = (0, a) if b is U else (a, b)
        if high < low:
            raise ValueError("Random range maximum is below minimum")
        span = high - low
        sample = self.NextDouble() if span <= MAX else self.GetSampleForLargeRange()
        return math.floor(sample * span) + low


def hash_string(value):
    return int32(xxhash.xxh32(value.encode("utf-8")).intdigest())


def hash_array(*values):
    return int32(
        xxhash.xxh32(
            struct.pack("<" + "i" * len(values), *(int32(v) for v in values))
        ).intdigest()
    )


def random_seed(legacy, *values):
    parts = [math.fmod(v, MAX) for v in values] + [0] * (5 - len(values))
    if legacy:
        return math.floor(math.fmod(sum(parts), MAX))
    return hash_array(*parts)


def install(environment, engine):
    def seed(*args):
        return random_seed(truth(get(engine["save"], "useLegacyRandom")), *args)

    def big_seed(*args):
        parts = []
        for a in args:
            if a is U:
                parts.append(0)
                continue
            n = a.value if isinstance(a, BigInt) else int(a)
            parts.append(n % MAX if n >= 0 else -((-n) % MAX))
        return seed(*parts)

    environment.local.update(
        {
            "CSRandom": CSRandom,
            "getRandomSeed": seed,
            "getRandomSeedFromBigInts": big_seed,
            "getHashFromString": hash_string,
            "getHashFromArray": hash_array,
            "bigIntToUnsigned32": lambda x: x.value & 0xFFFFFFFF,
            "bigIntToSigned32": lambda x: int32(x.value),
        }
    )
