# Packit Deploy

[![PyPI - Version](https://img.shields.io/pypi/v/packit-deploy.svg)](https://pypi.org/project/packit-deploy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/packit-deploy.svg)](https://pypi.org/project/packit-deploy)

-----

## Dev requirements

1. [Python3 >= 3.7](https://www.python.org/downloads/)
2. [Hatch](https://hatch.pypa.io/latest/install/)

## Test

```console
hatch run test
```

## Build

```console
hatch build
```

## Install from local sources

1. `hatch build`
2. `pip install dist/packit_deploy-{version}.tar.gz`

## Publish to PyPi

Ensure you have built a new version of the package:
1. `hatch clean`
2. `hatch build`

Then publish to the test server:

```console
hatch publish -r test
```

You will be prompted to enter your [test.pypi.org](https://test.pypi.org/legacy/) username and password.
To test the installation, first run Python in a container:

```
docker run --rm -it --entrypoint bash python
```

Then:

```
pip install --index-url https://test.pypi.org/simple packit-deploy
```

## Install from PyPi

```console
pip install packit-deploy
```
