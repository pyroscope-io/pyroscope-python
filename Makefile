.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf wheelhouse

.PHONY: build_wheel
build_wheel: clean
	python3 -m poetry build --format wheel

.PHONY: repair_wheel
repair_wheel:
	{ \
	auditwheel repair "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
	rm -rf ./dist; \
	mv ./wheelhouse ./dist; \
	}

.PHONY: build_sdist
build_sdist: clean
	python3 -m poetry build --format sdist
	{ \
		tar -tvf "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: install
install: build_wheel
	{ \
		python3 -m pip install --force-reinstall "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
	}

.PHONY: install-src
install-src: build_sdist
	{ \
		python3 -m pip install --force-reinstall "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: test
test:
	{ \
	python3 -m unittest test_wheel.py; \
	}

