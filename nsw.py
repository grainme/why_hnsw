from collections import deque
from random import shuffle
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
        # number of neighbors for each node
        self.m = m
        # exploration factor for search (bigger, better, slower)
        self.ef = ef
        self.nodes: List[Node] = []
        self.entry_point: Node

    def build(self, nodes: List[Node]):
        # Random shuffle means early nodes are scattered
        # across topics → better long-range coverage → better search.
        shuffle(nodes)
        for node in nodes:
            self.insert(node)

    def insert(self, new_node: Node):
        if len(self.nodes) == 0:
            self.entry_point = new_node
            self.nodes.append(new_node)
            return

        if len(self.nodes) < self.m:
            # connect new_nodes to all existing nodes, bidirectionally
            for node in self.nodes:
                new_node.neighbors.append(node)
                node.neighbors.append(new_node)
            self.nodes.append(new_node)
            return

        neighbors = self.search(new_node.vector, [self.entry_point], self.m)
        for neighbor in neighbors:
            new_node.neighbors.append(neighbor)
            neighbor.neighbors.append(new_node)
        self.nodes.append(new_node)

    def search(
        self, query: List[float], entry_points: List[Node], k: int
    ) -> List[Node]:
        """
        method that takes a query vector and navigates the graph to
        find th k closest nodes.

        1. candidates: "Who should I explore next?"
        2. results: "What are the best nodes I've found?"
        """

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

            # this is the clever part, i think.
            # The logic: if the closest thing left to explore is already worse
            # than everything in my results, then exploring it
            # (and its neighbors, which are likely even farther) can't possibly help.
            if closest_dist > furthest_dist:
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
