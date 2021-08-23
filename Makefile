.PHONY: test
test:
	rm -rf build
	poetry build --format wheel
	sleep 5
	pip3 install --force-reinstall dist/$(shell ls -1t dist | tail -n 1)
	python3 test.py
