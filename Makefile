.PHONY: all
# all: figures/runtime_mine.pdf figures/runtime_mine_manual.pdf figures/runtime_mine_notail.pdf figures/calpas/runtime_calpas.pdf figures/calpas/runtime_calpas_redo.pdf figures/runtime_all.pdf
all: figures/runtime_mine.pdf figures/calpas/runtime_calpas.pdf figures/runtime_all.pdf

responses:
	mkdir $@

figures:
	mkdir -p $@

figures/calpas:
	mkdir -p $@

# responses/%: scripts/fetch_%.sh responses
# 	sh $< > $@

figures/calpas/runtime_%.pdf: responses/% figures/% scripts/plot_runtime.py
	python scripts/plot_runtime.py $< $@

figures/runtime_%.pdf: responses/% figures scripts/plot_runtime.py
	python scripts/plot_runtime.py $< $@
