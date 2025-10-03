#!/usr/bin/env python3
"""
wordle_ranker.py
----------------
Drop‑in replacement for your original Wordle‑scoring script.

Key points
~~~~~~~~~~
* **Vectorised NumPy kernel** – no Python loops in the hot path.
* **Automatic multiprocessing** across all logical CPU cores.
* Only needs **pandas** and **numpy** – nothing else.
* Simple CLI flags for file locations, core count and result length.

Example
~~~~~~~
    python wordle_ranker.py \
        --valid wordle-words-main/valid-words.csv \
        --win   wordle-words-main/word-bank.csv \
        --top   20
"""

from __future__ import annotations

import argparse
import math
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def _filter_five_letter(df: pd.DataFrame) -> List[str]:
    """Return a list of the 5‑letter words in the *word* column / index."""
    col = df.columns[0] if "word" not in df.columns else "word"
    series = df.index if col == "word" else df[col]
    return series[series.str.len() == 5].str.lower().tolist()


def _words_to_uint8_matrix(words: List[str]) -> np.ndarray:
    """Return an (N, 5) uint8 matrix of ASCII codes for each word."""
    return np.frombuffer("".join(words).encode("ascii"), dtype=np.uint8).reshape(-1, 5)


def _score_block(valid_block: List[str], goal_matrix: np.ndarray) -> np.ndarray:
    """Vectorised score for a subset of valid words (size ≤ few thousand).

    Replicates the original *evaluate* logic exactly:
    * greens  – correct letter & position
    * yellows – correct letter, wrong position
    * grays   – not in the goal word
    """
    vmat = _words_to_uint8_matrix(valid_block)  # (M, 5)

    # greens: (M,1,5) vs (1,G,5) → (M,G)
    greens = (vmat[:, None, :] == goal_matrix[None, :, :]).sum(-1)

    # yellows: letter‑level membership minus greens
    in_goal = np.isin(vmat[:, None, :], goal_matrix[None, :, :])
    yellows = in_goal.sum(-1) - greens

    grays = 5 - (greens + yellows)

    yellow_value = (5 - yellows - greens) / (5 + yellows + greens) * yellows
    gray_value = (26 - grays - yellows - greens) * grays

    # Sum across every possible answer: (M,G) → (M,)
    return (yellow_value + gray_value).sum(-1, dtype=np.float64)


# --------------------------------------------------------------------------- #
# Main orchestrator
# --------------------------------------------------------------------------- #


def rank_words(
    valid_words: List[str],
    goal_words: List[str],
    n_jobs: int | None = None,
) -> pd.DataFrame:
    """Return DataFrame <word,value> sorted ascending by *value*."""
    goal_mat = _words_to_uint8_matrix(goal_words)

    n_total = len(valid_words)
    cpu = os.cpu_count() or 1
    n_jobs = cpu if n_jobs in (None, -1, 0) else max(1, n_jobs)
    n_jobs = min(n_jobs, cpu)

    if n_jobs == 1 or n_total < 1000:
        scores = _score_block(valid_words, goal_mat)
    else:
        chunk = math.ceil(n_total / n_jobs)
        slices = [valid_words[i : i + chunk] for i in range(0, n_total, chunk)]

        with ProcessPoolExecutor(max_workers=n_jobs) as exe:
            parts = list(exe.map(_score_block, slices, [goal_mat] * len(slices)))
        scores = np.concatenate(parts)

    df = pd.DataFrame({"word": valid_words, "value": scores})
    return df.sort_values("value", ascending=True, ignore_index=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Rank Wordle guesses by expected information gain."
    )
    parser.add_argument(
        "--valid",
        default="wordle-words-main/valid-words.csv",
        help="CSV file containing all allowed guess words (default: %(default)s)",
    )
    parser.add_argument(
        "--win",
        default="wordle-words-main/word-bank.csv",
        help="CSV file containing the answer list (default: %(default)s)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Print the top‑N words (default: %(default)s)",
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=-1,
        help="Number of worker processes (‑1 → all cores, default). 0 = single‑core.",
    )
    args = parser.parse_args()

    # Load CSVs
    valid_df = pd.read_csv(args.valid, header=None, names=["word"], dtype="string")
    win_df = pd.read_csv(args.win, header=None, names=["word"], dtype="string")

    valid_words = _filter_five_letter(valid_df)
    goal_words = _filter_five_letter(win_df)

    ranking = rank_words(valid_words, goal_words, n_jobs=args.jobs)

    pd.set_option("display.float_format", lambda v: f"{v:,.0f}")
    print(ranking.head(args.top).to_string(index=False))


if __name__ == "__main__":
    main()
