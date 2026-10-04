"""64-KiB LZX decoder, ported from MonoGame's LzxDecoder.cs.

Derived from libmspack: (C) 2003–2004 Stuart Caie; (C) 2011 Ali Scissons.
LZX was created by Jonathan Forbes and Tomi Poutanen, adapted by Microsoft.
Redistribute/modify under LGPL 2.1 or MS-PL; see THIRD_PARTY_NOTICES.md.
This port selects MS-PL. Copyright notices and this header must be retained.
The original author authorized adaptation of libmspack lzxd.c changes under
the same dual licensing scheme. Canonical Huffman decoding replaces the
reference's lookup-table optimization; state and offset transitions are retained.
"""

import struct


class Bits:
    def __init__(self, data):
        self.data, self.pos, self.buffer, self.left = data, 0, 0, 0

    def read(self, count):
        while self.left < count:
            if self.pos + 2 > len(self.data):
                raise ValueError("Truncated LZX bitstream.")
            word = self.data[self.pos] | self.data[self.pos + 1] << 8
            self.pos += 2
            self.buffer = self.buffer << 16 | word
            self.left += 16
        self.left -= count
        value = self.buffer >> self.left
        self.buffer &= (1 << self.left) - 1
        return value

    def raw(self, count):
        if self.pos + count > len(self.data):
            raise ValueError("Truncated LZX uncompressed block.")
        value = self.data[self.pos : self.pos + count]
        self.pos += count
        return value

    def align_uncompressed(self):
        # The format discards 1..16 bits, including a whole word if aligned.
        self.read(self.left if self.left else 16)
        self.buffer = self.left = 0


class Huffman:
    def __init__(self, lengths):
        self.codes = {}
        code = 0
        for width in range(1, 17):
            for symbol, length in enumerate(lengths):
                if length == width:
                    if code >= 1 << width:
                        raise ValueError("Oversubscribed LZX Huffman tree.")
                    self.codes[width, code] = symbol
                    code += 1
            code <<= 1
        if code and code != 1 << 17:
            raise ValueError("Incomplete LZX Huffman tree.")

    def read(self, bits):
        code = 0
        for width in range(1, 17):
            code = code << 1 | bits.read(1)
            symbol = self.codes.get((width, code))
            if symbol is not None:
                return symbol
        raise ValueError("Invalid LZX Huffman symbol.")


def read_lengths(lengths, first, last, bits):
    tree = Huffman([bits.read(4) for _ in range(20)])
    x = first
    while x < last:
        symbol = tree.read(bits)
        if symbol == 17:
            count, value = bits.read(4) + 4, 0
        elif symbol == 18:
            count, value = bits.read(5) + 20, 0
        elif symbol == 19:
            count = bits.read(1) + 4
            value = (lengths[x] - tree.read(bits)) % 17
        else:
            count, value = 1, (lengths[x] - symbol) % 17
        if x + count > last:
            raise ValueError("LZX code-length run exceeds tree.")
        lengths[x : x + count] = [value] * count
        x += count


class LzxDecoder:
    def __init__(self):
        self.window = bytearray([0xDC]) * 65536
        self.pos = 0
        self.repeated = [1, 1, 1]
        self.header = False
        self.remaining = self.block_length = self.block_type = 0
        self.main_lengths, self.length_lengths = [0] * 512, [0] * 249
        self.extra = [max(0, i // 2 - 1) for i in range(32)]
        self.bases = [0]
        for extra in self.extra[:-1]:
            self.bases.append(self.bases[-1] + (1 << extra))

    def decompress(self, data, output_size):
        if not 0 < output_size <= 32768:
            raise ValueError("Invalid LZX frame size.")
        bits = Bits(data)
        if not self.header:
            if bits.read(1):
                # MonoGame's Intel transform is unfinished, outside XNB tables.
                raise ValueError("LZX Intel E8 preprocessing is unsupported.")
            self.header = True
        out = bytearray()
        while len(out) < output_size:
            if self.remaining == 0:
                if self.block_type == 3 and self.block_length & 1:
                    bits.raw(1)
                self.block_type = bits.read(3)
                self.block_length = self.remaining = bits.read(16) << 8 | bits.read(8)
                if not self.remaining:
                    raise ValueError("Empty LZX block.")
                if self.block_type in (1, 2):
                    if self.block_type == 2:
                        self.aligned = Huffman([bits.read(3) for _ in range(8)])
                    read_lengths(self.main_lengths, 0, 256, bits)
                    read_lengths(self.main_lengths, 256, 512, bits)
                    self.main = Huffman(self.main_lengths)
                    read_lengths(self.length_lengths, 0, 249, bits)
                    self.length = Huffman(self.length_lengths)
                elif self.block_type == 3:
                    bits.align_uncompressed()
                    self.repeated = list(struct.unpack("<3I", bits.raw(12)))
                else:
                    raise ValueError("Invalid LZX block type.")
            count = min(self.remaining, output_size - len(out))
            self.remaining -= count
            if self.block_type == 3:
                raw = bits.raw(count)
                for value in raw:
                    self.window[self.pos] = value
                    self.pos = (self.pos + 1) & 65535
                out.extend(raw)
                continue
            while count:
                symbol = self.main.read(bits)
                if symbol < 256:
                    self.window[self.pos] = symbol
                    self.pos = (self.pos + 1) & 65535
                    out.append(symbol)
                    count -= 1
                    continue
                symbol -= 256
                length = symbol & 7
                if length == 7:
                    length += self.length.read(bits)
                length += 2
                slot = symbol >> 3
                if slot < 3:
                    offset = self.repeated[slot]
                    if slot:
                        self.repeated[slot] = self.repeated[0]
                        self.repeated[0] = offset
                else:
                    extra = self.extra[slot]
                    offset = self.bases[slot] - 2
                    if self.block_type == 2 and extra >= 3:
                        offset += (bits.read(extra - 3) << 3) + self.aligned.read(bits)
                    elif extra:
                        offset += bits.read(extra)
                    else:
                        offset = 1
                    self.repeated = [offset, self.repeated[0], self.repeated[1]]
                if length > count or not 1 <= offset <= 65536:
                    raise ValueError("Invalid LZX match.")
                count -= length
                for _ in range(length):
                    value = self.window[(self.pos - offset) & 65535]
                    self.window[self.pos] = value
                    self.pos = (self.pos + 1) & 65535
                    out.append(value)
        return bytes(out)


def decompress_frames(data, expected):
    decoder, out, pos = LzxDecoder(), bytearray(), 0
    while pos < len(data):
        if pos + 2 > len(data):
            raise ValueError("Truncated XNB LZX frame header.")
        hi, lo = data[pos : pos + 2]
        pos += 2
        frame_size, block_size = 32768, hi << 8 | lo
        if hi == 255:
            if pos + 3 > len(data):
                raise ValueError("Truncated XNB LZX extended header.")
            frame_size = lo << 8 | data[pos]
            block_size = data[pos + 1] << 8 | data[pos + 2]
            pos += 3
        if not frame_size or not block_size:
            if any(data[pos:]):
                raise ValueError("Data after XNB LZX terminator.")
            break
        if pos + block_size > len(data) or len(out) + frame_size > expected:
            raise ValueError("Invalid XNB LZX frame length.")
        out.extend(decoder.decompress(data[pos : pos + block_size], frame_size))
        pos += block_size
    if len(out) != expected:
        raise ValueError("XNB decompressed size mismatch.")
    return bytes(out)
