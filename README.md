# pyroscope-python

This is a repo for pyroscope python integration. It is currently under development and is not yet released. 
Version of Pyroscope library: <sha>

## Usage

### Build & publish

```sh
docker build --build-arg python_version=3.9 -t pyroscope-python .
docker run pyroscope-python publish --username <username> --password <password>
```

#### Or to publish to custom repository
```sh
docker run -e POETRY_PYPI_TOKEN_TEST="<token>" -e POETRY_REPOSITORIES_TEST_URL="https://test.pypi.org/legacy/" pyroscope-python publish -r test
```

### Install from pip
```sh
python3 -m pip install pyroscope
```
or:  
```sh
python3 -m pip install --index-url https://test.pypi.org/simple/ pyroscope
```

### Use API
```python
import os
import pyroscope_io as pyro
pid = os.getpid()
pyro.configure(pyro.Config("test name", "http://localhost:4040"))
pyro.start()
pyro.change_name("test name1")
pyro.stop()

```
