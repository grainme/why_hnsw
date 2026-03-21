from collections import deque
from typing import List

from utils import MaxHeap, MinHeap, Node, euclidean_distance

queries = [
    "best response to e4",
    "how to attack the king in the middlegame",
    "what is a fork in chess",
    "how do pawns affect the position",
    "endgame technique with rooks",
]
distance_computations = 0


class NSW:
    def __init__(self, m: int, ef: int) -> None:
        self.m = m
        self.ef = ef

    def build(self):
        # TODO
        return

    def insert(self):
        # TODO
        return

    """
        method that takes a query vector and navigates the graph to
        find th k closest nodes.

        1. candidates: a min-heap (closest first). "Who should I explore next?" Always the nearest unexplored node.
        2. results: a max-heap bounded by self.ef. "What are the best nodes I've found?" The max-heap lets you cheaply evict the worst when it overflows ef.

        NOTES:
            - bigger ef, better recall, more computation.
    """

    def search(
        self, query: List[float], entry_points: List[Node], k: int
    ) -> List[Node]:
        # keyed by dist to query
        candidates = MinHeap()
        # keyed by dist to query, bounded by efSearch
        results = MaxHeap()
        visited = set()

        for ep in entry_points:
            dist = euclidean_distance(query, ep.vector)
            # TODO: right now, we're storing the whole node, we can do ep.id instead, if needed.
            # but in that case, i need to add a method to fetch node by its Id...
            candidates.push((ep, dist))
            results.push((ep, dist))
            if len(results) > self.ef:
                results.pop_max()
            visited.add(ep.id)

        while candidates:
            closest_node, closest_dist = candidates.pop_min()
            furthest_node, furthest_dist = results.peek_max()

            if closest_dist > furthest_dist:
                # nothing left can improve the result??
                break

            for neighbor in closest_node.neighbors:
                if neighbor.id not in visited:
                    visited.add(neighbor.id)
                    dist = euclidean_distance(neighbor.vector, query)

                    if len(results) < self.ef or dist < furthest_dist:
                        candidates.push((neighbor, dist))
                        results.push((neighbor, dist))
                        if len(results) > self.ef:
                            results.pop_max()

        topK_closest = deque()
        while results:
            ep, dist = results.pop_max()
            topK_closest.appendleft(ep)

        return list(topK_closest)[:k]


def main():
    print()


if __name__ == "__main__":
    main()
