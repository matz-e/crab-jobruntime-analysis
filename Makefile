.PHONY: all
all: figures/runtime_mine.png figures/runtime_mine_manual.png figures/runtime_mine_notail.png figures/calpas/runtime_calpas.png figures/calpas/runtime_calpas_redo.png figures/runtime_all.png

responses:
	mkdir $@

figures:
	mkdir -p $@

figures/calpas:
	mkdir -p $@

responses/%: scripts/fetch_%.sh responses
	sh $< > $@

figures/calpas/runtime_%.png: responses/% figures/% scripts/plot_runtime.py
	python scripts/plot_runtime.py $< $@

figures/runtime_%.png: responses/% figures scripts/plot_runtime.py
	python scripts/plot_runtime.py $< $@
