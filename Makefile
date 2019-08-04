.PHONY: default

default: cv.pdf

cv.pdf: cv.tex
	pdflatex $<
