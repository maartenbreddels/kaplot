default:

font: kaplot/text/fontfamilies.py

all: quickdoc.wiki kaplot/quickgen.py kaplot/text/fontfamilies.py examples

EXAMPLES = examples/contour.py examples/fitsimage1.py examples/fitsimage2.py examples/graph1.py \
		examples/graph2.py examples/graphs.py examples/histogram.py examples/planck.py \
		examples/vectorfield.py examples/wcs1.py
EXAMPLE_TARGETS = $(patsubst %.py,doc/%.png,${EXAMPLES}) $(patsubst %.py,doc/%.eps,${EXAMPLES})


doc/examples/%.eps : examples/%.py
	python $< --hardcopy=doc/examples/$*.eps --debug=0 > hoeba
doc/examples/%.png : examples/%.py
	python $< --hardcopy=doc/examples/$*.png --debug=0 > hoeba

kaplot/quickgen.py: kaplot/objects/*.py kaplot/astro/*.py
	python utils/generatequicksource.py > $@
	
kaplot/text/fontfamilies.py:
	python kaplot/text/fonts.py > $@
	
quickdoc.wiki: kaplot/quick.py kaplot/quickgen.py 
	python utils/quickdoc.py > $@
	
examples: kaplot/quickgen.py ${EXAMPLE_TARGETS}

clean:
	rm ${EXAMPLE_TARGETS}
	rm quickdoc.wiki kaplot/quickgen.py kaplot/text/fontfamilies.py