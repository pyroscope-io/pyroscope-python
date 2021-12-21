.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf wheelhouse

.PHONY: build-src
build-src: clean
	poetry build --format sdist
	{ \
		tar -tvf "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: build
build: clean
	poetry build --format wheel
	{ \
		unzip -l "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		auditwheel show "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		auditwheel repair "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		unzip -l "wheelhouse/$$(ls -1t wheelhouse | grep whl | head -n 1)"; \
	}

.PHONY: install
install: build
	{ \
		pip3 install --force-reinstall "wheelhouse/$$(ls -1t wheelhouse | grep whl | head -n 1)"; \
	}

.PHONY: install-src
install-src: build-src
	{ \
		pip3 install --force-reinstall "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: test
test: install
	python3 tests/test.py

.PHONY: test-src
test-src: install-src
	python3 tests/test.py
