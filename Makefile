tester:
	@poetry run python3 -m unittest test

test: tester
	@echo ""