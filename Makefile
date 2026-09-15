# Test runner shortcuts (uv + the active virtual environment).
#
# Usage:
#    make test                     # run the whole unittest suite (discovery)
#    make test T=generator.unittests.utilities.test_align_country_codes.py
#    make test T=...test_align_country_codes.Test_align_country_codes   # a single case

UV := uv run --active

.PHONY: test

test:
ifdef T
    $(UV) python -m unittest $(T)
else
	$(UV) python -m unittest discover generator
endif