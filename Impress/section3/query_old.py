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
    VALUES ?itemType {{ wd:Q6 }}
        ?item wdt:P3+ wd:{castle_ID};
        wdt:P1 ?itemType .
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

def filter(rs):
    # Cache photos
    for row in rs["bindings"]:
        obj = URLCache(row["photo"])
        row["photo"] = os.path.basename(obj.cache_file)

    # Ensemble name
    d = {"castle_label": rs["bindings"][0]["castleLabel"]}

    # Bindings by ceiling painting parent
    bindings = {}
    for row in rs["bindings"]:
        parentLabel = row["parentLabel"]
        if parentLabel not in bindings:
            bindings[parentLabel] = {"parent": row["parent"]}
            bindings[parentLabel]["painting"] = {}

        itemLabel = row["itemLabel"]
        if itemLabel not in bindings[parentLabel]["painting"]:
            bindings[parentLabel]["painting"][itemLabel] = []

        bindings[parentLabel]["painting"][itemLabel].append(row)

    # Sort parents
    for key in sorted(bindings):
        bindings[key] = bindings.pop(key)

    # Sort ceiling paintings
    for parentLabel in bindings:
        for key in sorted(bindings[parentLabel]["painting"]):
            bindings[parentLabel]["painting"][key] = \
                bindings[parentLabel]["painting"].pop(key)

    d["bindings"] = bindings

    return d

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
