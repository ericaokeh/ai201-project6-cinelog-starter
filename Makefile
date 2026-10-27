PYTHON ?= python3

.PHONY: check test-unit

check:
	$(PYTHON) -m py_compile app.py models.py routes/watchlist/watchlist.py services/watchlist_service.py tests/test_watchlist.py

test-unit:
	$(PYTHON) -m pytest -q
