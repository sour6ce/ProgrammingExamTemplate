# Find all directories containing text.qmd files
QMD_DIRS := $(shell find . -maxdepth 1 -type d ! -name '.' ! -name 'zips' -exec test -f {}/text.qmd \; -print)
QMD_FILES := $(foreach dir,$(QMD_DIRS),$(dir)/text.qmd)
PDF_FILES := $(foreach dir,$(QMD_DIRS),$(dir)/text.pdf)

.PHONY: build
build: $(PDF_FILES)

# Pattern rule to render each text.qmd file
%/text.pdf: %/text.qmd
	quarto render $<

.PHONY: package
package: build
	python packing.py

.PHONY: package-folder
package-folder: build
	python packing.py --folder

.PHONY: clean
clean:
	rm -f $(PDF_FILES)

.PHONY: clean-packages
clean-packages:
	rm -rf zips packages