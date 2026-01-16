#!/usr/bin/env python3
import json
from collections import Counter, defaultdict
from pathlib import Path

# ========= CONFIGURE THIS IF NEEDED =========
DATA_PATH = Path("data/meps_all_with_overrides.json")

# JSON field names – adjust if your file is different
FIELD_COUNTRY = "country"
FIELD_PARTY = "party"           # national party
FIELD_EU_GROUP = "euGroupFull"  # EU-level political group (e.g. "Greens/EFA")
FIELD_USES_X = "usesX"          # boolean: True if MEP is active/on X
# ===========================================


def load_meps(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def compute_stats(meps, group_field):
    """
    Compute, for a given group field (e.g. 'country'):
      - total number of MEPs in each group
      - number of MEPs on X in each group
      - percentage on X
    Returns a list of dicts with:
      { 'group': <name>, 'on_x': int, 'total': int, 'pct': float }
    """
    totals = Counter()
    on_x = Counter()

    for m in meps:
        group = m.get(group_field)
        if not group:  # skip if missing
            continue
        totals[group] += 1
        if m.get(FIELD_USES_X):
            on_x[group] += 1

    results = []
    for group, total in totals.items():
        count_on_x = on_x[group]
        pct = (count_on_x / total * 100) if total > 0 else 0.0
        results.append(
            {
                "group": group,
                "on_x": count_on_x,
                "total": total,
                "pct": pct,
            }
        )

    # Sort:
    # 1) percentage on X (desc)
    # 2) MEPs on X (desc)
    # 3) group name (asc)
    results.sort(key=lambda r: (-r["pct"], -r["on_x"], r["group"]))
    return results


def print_markdown_table(title, group_label, rows):
    """
    Print a markdown table with:
    Rank | <group_label> | MEPs on X | Total MEPs | % on X
    """
    print(f"## {title}\n")
    print(f"| Rank | {group_label} | MEPs on X | Total MEPs | % on X |")
    print("| --- | --- | --- | --- | --- |")

    for i, r in enumerate(rows, start=1):
        pct_str = f"{r['pct']:.1f}"
        print(f"| {i} | {r['group']} | {r['on_x']} | {r['total']} | {pct_str} |")

    print()  # blank line after table


def main():
    meps = load_meps(DATA_PATH)

    # Country ranking
    country_stats = compute_stats(meps, FIELD_COUNTRY)
    print_markdown_table(
        "Ranking by country (share of MEPs on X)",
        "Country",
        country_stats,
    )

    # National party ranking
    # party_stats = compute_stats(meps, FIELD_PARTY)
    # print_markdown_table(
    #     "Ranking by national party (share of MEPs on X)",
    #     "Party",
    #     party_stats,
    # )

    # EU group ranking
    eu_group_stats = compute_stats(meps, FIELD_EU_GROUP)
    print_markdown_table(
        "Ranking by EU group (share of MEPs on X)",
        "EU group",
        eu_group_stats,
    )


if __name__ == "__main__":
    main()
