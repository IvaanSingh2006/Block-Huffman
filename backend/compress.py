import heapq
from collections import Counter
import json

class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_tree(freq):
    heap = [Node(sym, freq[sym]) for sym in freq]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(heap, merged)

    return heap[0]


def generate_codes(root, prefix="", codebook=None):
    if codebook is None:
        codebook = {}

    if root is None:
        return codebook

    if root.symbol is not None:
        codebook[root.symbol] = prefix if prefix != "" else "0"
        return codebook

    generate_codes(root.left, prefix + "0", codebook)
    generate_codes(root.right, prefix + "1", codebook)

    return codebook

def create_blocks(data, block_size):
    return [data[i:i+block_size] for i in range(0, len(data), block_size)]




def compress_file(input_path, output_path, block_size=1):
    with open(input_path, "rb") as f:
        data = f.read()

    blocks = create_blocks(data, block_size)
    freq = Counter(blocks)
    tree = build_tree(freq)
    codes = generate_codes(tree)

    encoded = "".join(codes[block] for block in blocks)

    with open(output_path, "w") as f:
        f.write(encoded)
    codebook = {k.hex(): v for k, v in codes.items()}

    with open("outputs/metadata.json", "w") as f:
        json.dump({
            "codebook": codebook,
            "block_size": block_size
        }, f)