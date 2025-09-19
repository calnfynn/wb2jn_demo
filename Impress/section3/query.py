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
    PREFIX wd: <https://wikibase.kewl.org/entity/>
    PREFIX wdt: <https://wikibase.kewl.org/prop/direct/>
    PREFIX p: <https://wikibase.kewl.org/prop/>
    PREFIX ps: <https://wikibase.kewl.org/prop/statement/>
    PREFIX pq: <https://wikibase.kewl.org/prop/qualifier/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>

    SELECT DISTINCT ?item ?itemLabel ?itemDescription ?itemTypeLabel ?photo ?creator ?parent ?parentLabel ?castleLabel WHERE {{
      ?item (wdt:P3+) wd:{castle_ID};
            wdt:P1 ?itemType .
      OPTIONAL {{ ?item wdt:P3 ?parent. }}
      OPTIONAL {{
        ?item p:P6 ?statement.
        ?statement ps:P6 ?photo.
        OPTIONAL {{ ?statement pq:P11 ?creator. }}
      }}
      BIND(wd:{castle_ID} AS ?castle)
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de". }}
    }}
    ORDER BY (?item)
    """


def build_tree(rows):
    """
    Build a nested dict (pyramid) of items based on parent/child relationships.
    """
    nodes = {}
    children_map = {}

    # Prepare nodes and track children
    for row in rows:
        qid = row["item"]["value"].split("/")[-1]
        label = row.get("itemLabel", {}).get("value", qid)
        parent = row.get("parent", {}).get("value")
        parent_qid = parent.split("/")[-1] if parent else None

        # Cache photos
        if "photo" in row and "value" in row["photo"]:
            obj = URLCache(row["photo"]["value"])
            row["photo"] = os.path.basename(obj.cache_file)

        # Initialize node
        nodes[qid] = {
            "id": qid,
            "label": label,
            "description": row.get("itemDescription", {}).get("value"),
            "type": row.get("itemTypeLabel", {}).get("value"),
            "photo": row.get("photo"),
            "creator": row.get("creator", {}).get("value"),
            "children": []
        }

        # Track parent relationship
        if parent_qid:
            children_map.setdefault(parent_qid, []).append(qid)

    # Link children into parents
    for parent_qid, child_qids in children_map.items():
        if parent_qid in nodes:
            for cq in child_qids:
                if cq in nodes:
                    nodes[parent_qid]["children"].append(nodes[cq])

    # Find roots (no parent)
    roots = [
        node for qid, node in nodes.items()
        if all(qid not in child_qids for child_qids in children_map.values())
    ]

    return roots


def filter(rs):
    roots = build_tree(rs["bindings"])
    d = {"castle_label": rs["bindings"][0]["castleLabel"]["value"]}
    d["tree"] = roots
    return d


if __name__ == "__main__":
    main()
