.PHONY: test

test:
	rm -rf build
	rm -rf dist
	rm -rf wheelhouse

	poetry build --format sdist
	sleep 1
	{ \
		tar -tvf "dist/$$(ls -1t dist | grep tar.gz | head -n 1)"; \
	}

	poetry build --format wheel
	sleep 1
	{ \
		unzip -l "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		auditwheel show "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		auditwheel repair "dist/$$(ls -1t dist | grep whl | head -n 1)"; \
		unzip -l "wheelhouse/$$(ls -1t wheelhouse | grep whl | head -n 1)"; \
	}

	{ \
		pip3 install --force-reinstall "wheelhouse/$$(ls -1t wheelhouse | grep whl | head -n 1)"; \
	}

	python3 test.py
