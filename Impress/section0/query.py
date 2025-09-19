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
    SELECT DISTINCT ?item ?itemLabel ?itemDescription ?photo ?creator ?address WHERE {{
    VALUES ?item {{ wd:{castle_ID} }}
    ?item wdt:P5 ?address .
    OPTIONAL {{
        ?item p:P6 ?statement .
        ?statement ps:P6 ?photo .
        OPTIONAL {{ ?statement pq:P11 ?creator. }}
    }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "de" }}
    }}
    """

def filter(rs):
    # Cache photos
    for row in rs["bindings"]:
        obj = URLCache(row["photo"])
        row["photo"] = os.path.basename(obj.cache_file)

    return rs

if __name__=="__main__":
    main()

# vim: shiftwidth=4 tabstop=4 softtabstop=4 expandtab
