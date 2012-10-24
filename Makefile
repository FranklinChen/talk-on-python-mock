# Line numbers distracting
LANDSLIDE = landslide -i -l no --relative --copy-theme

html:	mock.html

# TODO: pdf coming out wrong
pdf:	mock.pdf

all:	html pdf

mock.html:	mock.md
	$(LANDSLIDE) -d $@ $<

mock.pdf:	mock.md
	$(LANDSLIDE) -d $@ $<

.PHONY:	all html pdf
