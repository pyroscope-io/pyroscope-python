.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf wheelhouse

.PHONY: build_wheel
build_wheel: clean
	poetry build --format wheel
	{ \
		auditwheel repair "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		rm -rf ./dist; \
		mv ./wheelhouse ./dist; \
	}

.PHONY: build_sdist
build_sdist: clean
	poetry build --format sdist
	{ \
		tar -tvf "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: install
install: build_wheel
	{ \
		pip3 install --force-reinstall "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
	}

.PHONY: install-src
install-src: build_sdist
	{ \
		pip3 install --force-reinstall "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

.PHONY: test
test:
	python3 -c "import pyroscope_io as pyroscope;\
	from time import sleep; pyroscope.configure(app_name=\"simple.python.app\",server_address=\"http://pyroscope:4040\");\
	sleep(10)" \
	| grep -i "upload profile"

