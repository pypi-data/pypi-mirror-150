# pyhelios: the Helios' toolbox

## Installation

```sh
pip install pyhelios
```

## Contributing

The pyhelios Python package is managed by awesome tools: [poetry](https://python-poetry.org/) and [tox](https://tox.wiki/en/latest/index.html).

1. Create a virtual environment using poetry.

```sh
poetry env use `which python`
```

2. Build the pyhelios Python package (sdist and wheel).

```sh
poetry build
```

2. Install in the previously created virtual environment.

```sh
poetry install
```

3. Run the tests.

```sh
poetry run python -m tox
```

4. Publish to the [Python Package Index](https://pypi.org/)

```sh
poetry publish
```

If necessary, [poetry](https://python-poetry.org/) can bump the version for you.
The new version should be a valid [semver](https://semver.org/) string or a valid bump rule: patch, minor, major, prepatch, preminor, premajor, prerelease.

```sh
poetry version patch[minor, major, prepatch, preminor, premajor, prerelease]
```