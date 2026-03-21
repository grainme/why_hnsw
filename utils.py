from heapq import heappop, heappush
from math import sqrt
from typing import List, Tuple


class Node:
    def __init__(
        self,
        id: int,
        text: str,
        vector: List[float],
        source: str,
        neighbors: List["Node"] | None = None,
    ) -> None:
        self.id = id
        self.text = text
        self.vector = vector
        self.source = source
        self.neighbors = neighbors if neighbors is not None else []


# for both the MinHeap and MaxHeap, val is a tuple (ep, d)
# i added node.id as a tiebreaker
class MinHeap:
    def __init__(self) -> None:
        self.buffer: List[tuple[float, int, Node]] = []
        self.length = 0

    def push(self, val: Tuple[Node, float]):
        heappush(self.buffer, (val[1], val[0].id, val[0]))
        self.length += 1

    def peek_min(self) -> Tuple[Node, float]:
        if not self.buffer:
            raise Exception("Heap is empty")

        dist, _, ep = self.buffer[0]
        return ep, dist

    def pop_min(self) -> Tuple[Node, float]:
        if not self.buffer:
            raise Exception("Heap is empty")

        dist, _, ep = heappop(self.buffer)
        self.length -= 1
        return ep, dist

    def __bool__(self):
        return self.length == 0

    def __len__(self):
        return self.length


class MaxHeap:
    def __init__(self) -> None:
        self.buffer: List[tuple[float, int, Node]] = []
        self.length = 0

    def push(self, val: Tuple[Node, float]):
        heappush(self.buffer, (-val[1], val[0].id, val[0]))
        self.length += 1

    def peek_max(self) -> Tuple[Node, float]:
        if not self.buffer:
            raise Exception("Heap is empty")

        dist, _, ep = self.buffer[0]
        return ep, -dist

    def pop_max(self) -> Tuple[Node, float]:
        if not self.buffer:
            raise Exception("Heap is empty")

        dist, _, ep = heappop(self.buffer)
        self.length -= 1
        return ep, -dist

    def __bool__(self):
        return self.length == 0

    def __len__(self):
        return self.length


def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    # we're using the same embedding model
    # which means dim(v1) = dim(v2)
    dist = 0
    for i in range(len(v1)):
        dist += pow(v1[i] - v2[i], 2)
    return sqrt(dist)
