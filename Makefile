.PHONY: all
all: figures/runtime_mine.png figures/runtime_calpas.png figures/runtime_all.png

responses:
	mkdir $@

figures:
	mkdir $@

responses/%: scripts/fetch_%.sh responses
	sh $< > $@

figures/runtime_%.png: responses/% figures scripts/plot_runtime.py
	python scripts/plot_runtime.py $< $@
