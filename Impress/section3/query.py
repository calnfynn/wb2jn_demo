#! /usr/bin/env python3
#
# Copyright (C) 2025 The Authors
# All rights reserved.
#
# This file is part of cps_coffeebook.
#
# cps_coffeebook is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation.
#
# cps_coffeebook is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with cps_coffeebook. If not, see http://www.gnu.org/licenses/
#
import os
from cps_impress.urlcache import URLCache


def main():
    pass


def query(args):
    # Default: Stuttgart, Schloss Solitude
    castle_ID = "Q68" if "castle_ID" not in args else args["castle_ID"]

    return f"""
    SELECT DISTINCT ?item ?itemLabel ?itemDescription ?itemTypeLabel ?photo ?creator ?parent ?parentLabel ?castleLabel
    WHERE {{
      {{ BIND(wd:Q68 AS ?item) }}
      UNION
      {{
        ?item (wdt:P3+) wd:Q68;
        wdt:P1 ?itemType .
      }}
      OPTIONAL {{ ?item wdt:P3 ?parent . }}
      OPTIONAL {{
        ?item p:P6 ?statement .
        ?statement ps:P6 ?photo .
        OPTIONAL {{ ?statement pq:P11 ?creator. }}
      }}
      BIND(wd:{castle_ID} AS ?castle)
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de" }}
    }}
    ORDER BY ?item
    """

def filter(rs, castle_id=None):
    bindings = [
        {k: (v["value"] if isinstance(v, dict) else v) for k, v in row.items()}
        for row in rs["bindings"]
    ]

    # Cache photos
    for row in bindings:
        if "photo" in row and row["photo"]:
            obj = URLCache(row["photo"])
            row["photo"] = os.path.basename(obj.cache_file)

    # Index by item ID
    items = {}
    for row in bindings:
        item_id = row["item"]
        if item_id not in items:
            items[item_id] = {
                "item": item_id,
                "itemLabel": row.get("itemLabel"),
                "itemDescription": row.get("itemDescription"),
                "itemTypeLabel": row.get("itemTypeLabel"),
                "photos": [],
            }
        if row.get("photo"):
            items[item_id]["photos"].append({
                "url": row["photo"],
                "creator": row.get("creator"),
            })

    # Group children by parent
    children_map = {}
    for row in bindings:
        parent = row.get("parent")
        if parent:
            children_map.setdefault(parent, set()).add(row["item"])

    def build_tree(item_id, seen=None):
        if seen is None:
            seen = set()
        if item_id in seen:
            return None  # skip cycles
        seen.add(item_id)

        row = items.get(item_id, {"itemLabel": None})
        node = {
            "id": item_id,
            "label": row.get("itemLabel") or row.get("parentLabel"),
            "description": row.get("itemDescription"),
            "type": row.get("itemTypeLabel"),
            "photos": row.get("photos"),
            "creator": row.get("creator"),
            "children": []
        }

        added_labels = set()
        for child_id in children_map.get(item_id, []):
            child_node = build_tree(child_id, seen.copy())
            if child_node and child_node["label"] not in added_labels:
                node["children"].append(child_node)
                added_labels.add(child_node["label"])

        return node

    if castle_id is None and bindings:
        castle_id = bindings[0].get("castle") or bindings[0]["item"]
    if not castle_id:
        return {"castle_label": None, "tree": None}

    root_uri = (
        castle_id if castle_id.startswith("http") else f"https://wikibase.kewl.org/entity/{castle_id}"
    )
    tree = build_tree(root_uri)

    return {
        "castle_label": bindings[0].get("castleLabel") if bindings else None,
        "tree": tree,
    }

