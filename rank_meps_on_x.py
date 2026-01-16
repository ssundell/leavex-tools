#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

# Path to your JSON file
DATA_PATH = Path("data/meps_all_with_overrides.json")

def load_meps(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def filter_meps_on_x(meps):
    """Keep only MEPs who are on X (usesX == True)."""
    return [m for m in meps if m.get("usesX")]

def rank_by_country(meps_on_x):
    """Return list of (country, count) sorted by count desc, then name."""
    counts = Counter(m["country"] for m in meps_on_x if m.get("country"))
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))

def rank_by_party(meps_on_x):
    """
    Return list of (party, count) sorted by count desc, then name.
    Using the 'party' field; switch to 'euGroupFull' if you prefer that.
    """
    counts = Counter(m["party"] for m in meps_on_x if m.get("party"))
    return sorted(counts.items(), key=lambda x: (-x[1], x[0]))

def print_markdown_table(title, header_cols, rows):
    """Print a simple markdown table to stdout."""
    print(f"## {title}")
    print()
    # Header
    print("| " + " | ".join(header_cols) + " |")
    print("| " + " | ".join("---" for _ in header_cols) + " |")
    # Rows
    for row in rows:
        print("| " + " | ".join(str(col) for col in row) + " |")
    print()  # blank line after table

def main():
    meps = load_meps(DATA_PATH)
    meps_on_x = filter_meps_on_x(meps)

    # Rankings
    country_ranking = rank_by_country(meps_on_x)
    party_ranking = rank_by_party(meps_on_x)

    # Prepare rows with rank numbers
    country_rows = [
        (rank, country, count)
        for rank, (country, count) in enumerate(country_ranking, start=1)
    ]
    party_rows = [
        (rank, party, count)
        for rank, (party, count) in enumerate(party_ranking, start=1)
    ]

    # Print tables
    print_markdown_table(
        "Ranking by country (MEPs on X)",
        ["Rank", "Country", "MEPs on X"],
        country_rows,
    )

    print_markdown_table(
        "Ranking by party (MEPs on X)",
        ["Rank", "Party", "MEPs on X"],
        party_rows,
    )

if __name__ == "__main__":
    main()
