.PHONY=pdflatex latex wordcount proof clean
NAME=uieda_barbosa
FIGS=

latex: ${NAME}.dvi
pdflatex: ${NAME}.pdf

${NAME}.pdf: ${NAME}.tex ${FIGS}
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex

${NAME}.dvi: ${NAME}.tex ${FIGS}
	latex ${NAME}.tex
	latex ${NAME}.tex
	latex ${NAME}.tex

dvi2pdf: ${NAME}.dvi
	dvipdf ${NAME}.dvi

wordcount:
	@detex ${NAME}.tex | wc -w

proof:
	@echo ""
	@echo "DUPLICATE ADJACENT WORDS:"
	@echo "------------------------"
	@-perl bin/duplicates ${NAME}.tex;
	@echo ""
	@echo "WEASEL WORDS:"
	@echo "------------------------"
	@-bash bin/weasel ${NAME}.tex;
	@echo ""
	@echo "PASSIVE VOICE:"
	@echo "------------------------"
	@-bash bin/passive ${NAME}.tex;

clean:
	rm -rf ${NAME}.pdf ${NAME}.dvi *.aux *.bbl *.log *.blg
