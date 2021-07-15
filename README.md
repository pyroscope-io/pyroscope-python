# pyroscope-python

This is a repo for pyroscope python integration. It is currently under development and is not yet released. 

Usage:  
`docker build -t pyroscope-python .`  
`docker run -e POETRY_PYPI_TOKEN="<token>" pyroscope-python publish` 

Or to publish to test repository:  
`docker run -e POETRY_PYPI_TOKEN_TEST="<token>" -e POETRY_REPOSITORIES_TEST_URL="https://test.pypi.org/legacy/" pyroscope-python publish -r test`

