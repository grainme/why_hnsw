# Jiwar

> **Jiwar** (جوار) — Arabic for "neighbor"

Vector similarity search algorithms, built from scratch.

The goal is to understand how nearest-neighbor search works under the hood — starting from brute force and progressing to graph-based approximate methods.

## How it works

A small chess knowledge base (openings, tactics, endgames) is chunked, embedded with `all-MiniLM-L6-V2`, and used as the test dataset.

**Algorithms implemented:**

| Module | Algorithm | Approach |
|---|---|---|
| `brute.py` | Brute Force | Compares query against every vector. O(n) per query — exact but slow. |
| `nsw.py` | Navigable Small World | Builds a graph where each node knows its `m` closest neighbors, then searches by hopping through edges. Approximate but fast. |
