NAME=uieda_barbosa
OUTPUT=uieda_barbosa.pdf
FIGS=

all: ${OUTPUT}


${OUTPUT}: ${NAME}.tex ${FIGS}
	pdflatex ${NAME}.tex
	pdflatex ${NAME}.tex
	mv ${NAME}.pdf ${OUTPUT}

wordcount: ${NAME}.tex
	@detex $< | wc -w

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
	rm -rf ${OUTPUT} *.aux *.bbl *.log *.blg
