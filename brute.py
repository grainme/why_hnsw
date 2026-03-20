from math import sqrt

from data import embedding_model, load_embeddings_from_json, queries

embeddings = load_embeddings_from_json()
distance_computations = 0


def euclidean_distance(v1, v2) -> float:
    # we're using the same embedding model
    # which means dim(v1) = dim(v2)
    dist = 0
    for i in range(len(v1)):
        dist += pow(v1[i] - v2[i], 2)
    return sqrt(dist)


def brute_force_search(query_vector, all_vectors, top_k=3):
    global distance_computations
    dist_per_pair = []

    for v in all_vectors:
        d = euclidean_distance(query_vector, v["vector"])
        distance_computations += 1
        dist_per_pair.append((query_vector, v, d))

    dist_per_pair.sort(key=lambda t: t[2])

    return dist_per_pair[:top_k]


def main():
    for q in queries:
        query_vector = embedding_model.embed_query(q)
        results = brute_force_search(query_vector, embeddings)

        print(f"Query: '{q}':")
        for idx, res in enumerate(results):
            print(f"{idx} - {res[2]} [{res[1]['source']}] '{res[1]['text'][:50]}...'")
        print("\n")

    print(f"Distance computation: {distance_computations}")


if __name__ == "__main__":
    main()
