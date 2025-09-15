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

SECTIONS := section1.qmd section3.qmd
# section2.qmd

book:$(SECTIONS)
	quarto render

$(SECTIONS):
	sparql section1 -n -t md -f section1.qmd
#	sparql section2 -n -t md -f section2.qmd
	sparql section3 -n -t md -f section3.qmd

# AMD64
setup:
	quarto install tinytex

clean:
	find -name "*~" -delete
	rm -Rf .quarto Docs
	rm -f $(SECTIONS) *.jpeg
	rm -f index.aux index.idx index.log index.pdf index.tex index.toc
