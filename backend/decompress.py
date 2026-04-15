import json

def decompress_file(input_path, output_path, metadata_path):
    with open(metadata_path, "r") as f:
        meta = json.load(f)

    codebook = meta["codebook"]
    block_size = meta["block_size"]
    padding = meta.get("padding", 0)

    reverse_codes = {
        v: bytes.fromhex(k) for k, v in codebook.items()
    }

    with open(input_path, "r") as f:
        encoded = f.read().strip()

    if padding:
        encoded = encoded[:-padding]

    current = ""
    decoded_bytes = bytearray()

    for bit in encoded:
        current += bit

        if current in reverse_codes:
            block = reverse_codes[current]

            if len(block) != block_size:
                print("Warning: block size mismatch")

            decoded_bytes.extend(block)
            current = ""

    if current != "":
        print("Warning: leftover bits detected")

    with open(output_path, "wb") as f:
        f.write(decoded_bytes)

    print("Decompression successful!")
    print("Decoded size:", len(decoded_bytes))