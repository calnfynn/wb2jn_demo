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

clean:
	cd Quarto && $(MAKE) clean
	cd Notebook && $(MAKE) clean
	find -type f -name "*~" -delete
	find -type f -name "*.pyc" -delete
	find -type d -name "__pycache__" -delete

install:
	python3 -m pip install -r requirements.txt

venv:
	python3 -m venv ~/.venvs/cps_coffeebook

ls:
	find -type f -not -path "./.git/*" -ls

quarto:
	cd Quarto && $(MAKE)

notebook:
	cd Notebook && jupyter-notebook
