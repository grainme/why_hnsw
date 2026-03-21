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

## Project structure

```
jiwar/
├── data.py              # Loads knowledge base, chunks, embeds, caches to embeddings.json
├── brute.py             # Brute force nearest-neighbor search
├── nsw.py               # Navigable Small World graph (WIP)
├── utils.py             # Distance functions (euclidean)
├── knowledge_base/      # Chess topic markdown files
│   ├── sicilian_defense.md
│   ├── queens_gambit.md
│   ├── kings_indian.md
│   ├── italian_game.md
│   ├── middlegame_strategy.md
│   ├── pawn_structure.md
│   ├── tactics.md
│   └── endgame_principles.md
└── embeddings.json      # Cached vectors (generated on first run)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Generate embeddings (only needed once):

```bash
python data.py
```

Run brute force search:

```bash
python brute.py
```
