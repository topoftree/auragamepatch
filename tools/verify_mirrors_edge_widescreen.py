#!/usr/bin/env python3
"""Verify external reference resources without redistributing game data.

Aspect float fix: https://www.wsgf.org/dr/mirrors-edge
UE3 chunk format also documented by MirrorsEdgeTweaks DecompressionService.cs
(upstream source retained in sources/). This independent validator uses lzokay,
not the Windows tool or its native DLL. No downloaded code is executed.
"""
import argparse
import hashlib
import json
import struct
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "recipes/mirrors-edge-2008/widescreen/mirrors-edge-widescreen-195/1.0.0/recipe.json"
ZIP_HASHES = {
    "Base": "e53fffb1af62e3f3284ba1877367e0e224ddec8c3402b3dbf441bd3a4d24c09e",
    "DLC": "54d95f53c230e44ae6b4cb209dca3bd216cdebf002142fd02804c0f5ad2878e3",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def decode(data):
    import lzokay
    require(len(data) <= 16 * 1024 * 1024, "Input too large")
    integer = lambda offset: struct.unpack_from("<I", data, offset)[0]
    require(integer(0) == 0x9E2A83C1 and struct.unpack_from("<HH", data, 4) == (536, 43), "Unknown UE3 header")
    flags = 16 + integer(12)
    generations = flags + 48
    require(0 < integer(generations) <= 4, "Unknown generations")
    compression = generations + 4 + integer(generations) * 12 + 8
    require(integer(compression) == 2, "Expected LZO chunks")
    count = integer(compression + 4)
    require(count == 5, "Unexpected chunk count")
    chunks = [struct.unpack_from("<IIII", data, compression + 8 + n * 16) for n in range(count)]
    size = max(u + n for u, n, _, _ in chunks)
    require(size <= 16 * 1024 * 1024, "Expanded size limit")
    output = bytearray(size)
    head = bytearray(data[:chunks[0][2]])
    struct.pack_into("<I", head, flags, integer(flags) & ~0x02000000)
    struct.pack_into("<II", head, compression, 0, 0)
    head[compression + 8:len(head) - count * 16] = head[compression + 8 + count * 16:]
    output[:chunks[0][0]] = head[:chunks[0][0]]
    previous_end = chunks[0][0]
    for offset, expanded, packed_offset, packed_size in chunks:
        require(offset == previous_end and offset + expanded <= size and packed_offset + packed_size <= len(data), "Chunk bounds")
        tag, block_size, compressed, uncompressed = struct.unpack_from("<IIII", data, packed_offset)
        require(tag == 0x9E2A83C1 and block_size == 131072 and uncompressed == expanded, "Invalid chunk header")
        blocks = (uncompressed + block_size - 1) // block_size
        require(0 < blocks <= 128, "Block limit")
        sizes = [struct.unpack_from("<II", data, packed_offset + 16 + j * 8) for j in range(blocks)]
        require(sum(x[0] for x in sizes) == compressed and sum(x[1] for x in sizes) == expanded, "Block sums")
        source = packed_offset + 16 + blocks * 8
        target = offset
        for packed, unpacked in sizes:
            require(0 < unpacked <= block_size and 0 < packed <= packed_size and source + packed <= packed_offset + packed_size, "Block bounds")
            block = lzokay.decompress(data[source:source + packed], unpacked)
            require(len(block) == unpacked, "Decompressed size")
            output[target:target + unpacked] = block
            source += packed
            target += unpacked
        require(source == packed_offset + packed_size and target == offset + expanded, "Chunk length")
        previous_end = target
    return bytes(output)


def apply(data, variant):
    require(len(data) == variant["bytes"] and sha(data) == variant["before"], "Unrecognized resource")
    edit, = variant["edits"]
    offset = edit["offset"]
    require(data[offset:offset + 4].hex() == edit["before"] == "f38ee33f", "Aspect bytes")
    require(edit["after"] == struct.pack("<f", 1560 / 720).hex(), "Wrong aspect ratio")
    result = data[:offset] + bytes.fromhex(edit["after"]) + data[offset + 4:]
    require(sha(result) == variant["after"], "Patched resource hash")
    return result


def verify(reference_dir):
    variants = json.loads(RECIPE.read_text())["resourceBinary"]["variants"]
    results = []
    for i, name in enumerate(("Base", "DLC")):
        path = reference_dir / (name + "_Engine.zip")
        require(path.stat().st_size < 2 * 1024 * 1024 and sha(path.read_bytes()) == ZIP_HASHES[name], "Reference ZIP hash")
        with zipfile.ZipFile(path) as archive:
            entry = archive.getinfo("TdGame/CookedPC/Engine.u")
            require(entry.file_size < 16 * 1024 * 1024, "Resource size")
            resource = archive.read(entry)
        patched = apply(resource, variants[i])
        before, after = decode(resource), decode(patched)
        expected = apply(before, variants[i + 2])
        require(after == expected, "Compressed edit changed other decoded data")
        changed = [j for j in range(len(before)) if before[j] != after[j]]
        require(changed == list(range(variants[i + 2]["edits"][0]["offset"], variants[i + 2]["edits"][0]["offset"] + 4)), "Unexpected decoded diff")
        results.append(dict(edition=name, compressedBefore=sha(resource), compressedAfter=sha(patched),
            decodedBefore=sha(before), decodedAfter=sha(after), decodedChangedBytes=len(changed),
            decodeSuccess=True, apkTested=False, phoneGameplayTested=False))
    return {"schema": 1, "aspect": "19.5:9", "results": results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-dir", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.reference_dir), indent=2))
