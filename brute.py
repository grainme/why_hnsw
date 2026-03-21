from dataclasses import dataclass
from typing import List

from langchain_huggingface import HuggingFaceEmbeddings

from data import embeddings
from utils import Node, euclidean_distance


@dataclass
class QueryVecDist:
    query_vector: List[float]
    candidate_vector: Node
    distance: float


queries = [
    "best response to e4",
    "how to attack the king in the middlegame",
    "what is a fork in chess",
    "how do pawns affect the position",
    "endgame technique with rooks",
]
distance_computations = 0


def brute_force_search(query: List[float], embeddings: List[Node], top_k=3):
    global distance_computations
    dist_per_pair: List[QueryVecDist] = []

    for embedding in embeddings:
        d = euclidean_distance(query, embedding.vector)
        distance_computations += 1
        dist_per_pair.append(QueryVecDist(query, embedding, d))

    dist_per_pair.sort(key=lambda t: t.distance)

    return dist_per_pair[:top_k]


def main():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-V2")

    for q in queries:
        query_vector = embedding_model.embed_query(q)
        results = brute_force_search(query_vector, embeddings)

        print(f"Query: '{q}':")
        for idx, res in enumerate(results):
            print(
                f"{idx} - {res.distance} [{res.candidate_vector.source}] '{res.candidate_vector.text[:50]}...'"
            )
        print("\n")

    print(f"Distance computation: {distance_computations}")


if __name__ == "__main__":
    main()
