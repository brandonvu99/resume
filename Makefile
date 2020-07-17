.PHONY: default clean

default: cv.pdf

clean:
	rm -rvf cv.pdf metadata.txt cv.pdf.fixed

cv.pdf: cv.tex
	pdflatex $<
	pdftk cv.pdf dump_data output metadata.txt
	sed -i 's/*0.5in//g; s/ ? $$//g' metadata.txt
	pdftk cv.pdf update_info metadata.txt output cv.pdf.fixed
	mv cv.pdf.fixed cv.pdf
	rm -v metadata.txt
