#!/usr/bin/env python3
"""
apply_meps_overrides.py

Merge manual overrides from meps_overrides.json into meps_all.json.

- Base file: meps_all.json   (list of MEP objects)
- Overrides: meps_overrides.json (object keyed by MEP id)
- Output:    meps_all_with_overrides.json

Behavior:
- For each override entry:
  - If the id exists in the base list, update that object with all override keys.
  - If the id does NOT exist in the base list, create a new stub object and append it.
"""

import json
from pathlib import Path

BASE_FILE = Path("data/meps_all.json")
OVERRIDES_FILE = Path("data/meps_overrides.json")
OUTPUT_FILE = Path("data/meps_all_with_overrides.json")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    if not BASE_FILE.exists():
        raise SystemExit(f"Base file not found: {BASE_FILE}")
    if not OVERRIDES_FILE.exists():
        raise SystemExit(f"Overrides file not found: {OVERRIDES_FILE}")

    base_data = load_json(BASE_FILE)
    overrides = load_json(OVERRIDES_FILE)

    if not isinstance(base_data, list):
        raise SystemExit("meps_all.json must be a JSON array (list of objects).")
    if not isinstance(overrides, dict):
        raise SystemExit("meps_overrides.json must be a JSON object keyed by MEP id.")

    # Index base data by id for fast lookup
    index = {}
    for obj in base_data:
        obj_id = obj.get("id")
        if obj_id:
            if obj_id in index:
                print(f"[WARN] Duplicate id in base data: {obj_id}")
            index[obj_id] = obj

    # Apply overrides
    for mep_id, override_data in overrides.items():
        if not isinstance(override_data, dict):
            print(f"[WARN] Override for {mep_id} is not an object, skipping.")
            continue

        if mep_id in index:
            base_obj = index[mep_id]
            print(f"[INFO] Applying override to existing MEP: {mep_id}")
            # Shallow merge: override / add keys onto the base object
            for key, value in override_data.items():
                base_obj[key] = value
        else:
            print(f"[WARN] Override id {mep_id} not found in base data; creating stub entry.")
            # Create a new minimal object and append it
            new_obj = {"id": mep_id}
            new_obj.update(override_data)
            base_data.append(new_obj)
            index[mep_id] = new_obj

    # Write merged output
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)

    print(f"[INFO] Wrote merged data with overrides to {OUTPUT_FILE}")
    print(f"[INFO] Total records: {len(base_data)}")


if __name__ == "__main__":
    main()
