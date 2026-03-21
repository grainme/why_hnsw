"""
> the main job of this file, is loading nodes from embeddings.json
"""

import json
from typing import List

from utils import Node


# load vector from embedding.json
def _load_embeddings_from_json() -> List[Node]:
    with open("embeddings.json", "r") as f:
        data = json.load(f)

        embeddings: List[Node] = []
        for e in data:
            node = Node(e["id"], e["text"], e["vector"], e["source"])
            embeddings.append(node)
        return embeddings


embeddings = _load_embeddings_from_json()
