# pyroscope-python

This is a repo for pyroscope python integration. It is currently under development and is not yet released. 
Version of Pyroscope library: <sha>

## Usage

### Build & publish

```sh
docker build --build-arg pyroscope_libs_sha=<sha> -t pyroscope-python .
docker run -e POETRY_PYPI_TOKEN="<token>" pyroscope-python publish
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
from pyroscope import agent
pid = os.getpid()
agent.start("test name", pid, "http://localhost:4040", "auth-token", 100, 1, "debug")
agent.change_name("test name1")
agent.stop(pid)

```
