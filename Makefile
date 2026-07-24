TEX2PDF = latexmk

MAINFILE = main.tex
MAINTARGET = $(MAINFILE:.tex=.pdf)
SUBFILEDIR = sub
SUBFILES = $(wildcard $(SUBFILEDIR)/*.tex)
SUBTARGETS = $(SUBFILES:.tex=.pdf)

BIBFILES = $(wildcard *.bib)

FIGDIR = fig
SVGFILES = $(wildcard $(FIGDIR)/*.svg)
PNGFILES = $(wildcard $(FIGDIR)/*.png)
JPGFILES = $(wildcard $(FIGDIR)/*.jpg)
SVG2PDFTARGETS = $(SVGFILES:.svg=.pdf)
DEPFILES = $(SVG2PDFTARGETS) $(PNGFILES) $(JPGFILES) $(BIBFILES)

main: $(MAINTARGET)

$(MAINTARGET): $(SUBFILES)

subs: $(SUBTARGETS)

all: main subs

dep: $(DEPFILES)

ifeq ($(findstring 1.,$(shell inkscape -V 2>/dev/null)),)
%.pdf: %.svg
	DISPLAY= inkscape -z -D -A $(abspath $@) $(abspath $<)
else
%.pdf: %.svg
	DISPLAY= inkscape -D -o $(abspath $@) $(abspath $<)
endif

%.pdf: %.tex $(DEPFILES)
	cd $(dir $<) && \
		$(TEX2PDF) $(notdir $<) && \
		ln -sf .tmp/$(notdir $@)

%.tex: %.input_tex
	sed -n 1,/\begin{document}/p $(MAINFILE) > $@
	echo '\maketitle' >> $@
	cat $< >> $@
	sed -n /\end{document}/,$$$$p $(MAINFILE) >> $@
	# Make main.pdf
	cd `git rev-parse --show-toplevel` && make main

arrange:
	rm -rfv .tmp/* */.tmp/*
	rm -fv $(SVG2PDFTARGETS)

clean: arrange
	rm -fv *.pdf $(SUBFILEDIR)/*.pdf
