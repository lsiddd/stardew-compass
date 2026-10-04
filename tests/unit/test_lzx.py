import struct
import pytest
from stardew.infrastructure.xnb.lzx import LzxDecoder, decompress_frames


class BitWriter:
    def __init__(self):
        self.bits = ""

    def write(self, value, count):
        self.bits += f"{value:0{count}b}"

    def finish(self):
        bits = self.bits + "0" * (-len(self.bits) % 16)
        return b"".join(
            struct.pack("<H", int(bits[i : i + 16], 2)) for i in range(0, len(bits), 16)
        )


def tree(w, count, delta):
    for length in [4] * 16 + [0] * 4:
        w.write(length, 4)
    for _ in range(count):
        w.write(delta, 4)


def compressed_block(aligned=False):
    # Full nine-bit main tree; the pre-tree uses all 16 four-bit symbols.
    w = BitWriter()
    w.write(0, 1)
    w.write(2 if aligned else 1, 3)
    w.write(0, 16)
    w.write(22, 8)
    if aligned:
        for _ in range(8):
            w.write(3, 3)
    tree(w, 256, 8)  # previous 0 - delta 8 mod 17 = length 9
    tree(w, 256, 8)
    tree(w, 249, 0)
    for ch in b"abcdefghijklmnopqrst":
        w.write(ch, 9)
    w.write(256 + (8 << 3), 9)  # two-byte match, explicit offset slot 8
    w.write(0, 3)  # offset 14, verbatim bits or aligned symbol 0
    return w.finish()


@pytest.mark.parametrize("aligned", [False, True])
def test_lzx_literal_and_offset(aligned):
    assert (
        LzxDecoder().decompress(compressed_block(aligned), 22)
        == b"abcdefghijklmnopqrstgh"
    )


def uncompressed_block(data):
    w = BitWriter()
    w.write(0, 1)
    w.write(3, 3)
    w.write(len(data) >> 8, 16)
    w.write(len(data) & 255, 8)
    return w.finish() + struct.pack("<3I", 1, 1, 1) + data


def test_lzx_window_and_state_across_frames():
    data = bytes(range(256)) * 384  # three full frames; wraps the 64-KiB window
    block = uncompressed_block(data)
    # First frame includes 16 bytes of header, subsequent frames only raw bytes.
    chunks = [block[: 16 + 32768], block[16 + 32768 : 16 + 65536], block[16 + 65536 :]]
    framed = b"".join(struct.pack(">H", len(chunk)) + chunk for chunk in chunks)
    assert decompress_frames(framed, len(data)) == data


def test_lzx_repeated_offset_survives_frame_boundary():
    w = BitWriter()
    w.write(0, 1)
    w.write(1, 3)
    w.write(0, 16)
    w.write(10, 8)
    tree(w, 256, 8)
    tree(w, 256, 8)
    tree(w, 249, 0)
    w.write(ord("A"), 9)
    first = w.finish()
    # Three length-3 matches, each using the persisted R0 offset.
    second = BitWriter()
    for _ in range(3):
        second.write(256 + 1, 9)
    decoder = LzxDecoder()
    assert decoder.decompress(first, 1) == b"A"
    assert decoder.decompress(second.finish(), 9) == b"A" * 9


def test_lzx_extended_frame_and_padding():
    data = b"synthetic"
    block = uncompressed_block(data)
    frame = b"\xff" + struct.pack(">HH", len(data), len(block)) + block
    assert decompress_frames(frame + bytes(4), len(data)) == data
    with pytest.raises(ValueError):
        decompress_frames(frame[:-1], len(data))
    with pytest.raises(ValueError):
        decompress_frames(frame, len(data) + 1)
    with pytest.raises(ValueError):
        decompress_frames(frame + bytes(4) + b"x", len(data))
