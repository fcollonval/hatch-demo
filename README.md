# Hatch Demo

This is a demonstrator for [hatch](https://hatch.pypa.io) hooks presented at Python Rennes Meetup 04-2024.

The example is a server specified through [openAPI v3.0](https://spec.openapis.org/oas/v3.0.3.html)
specification using [connexion](https://connexion.readthedocs.io).

The hatch hook examples are:
- [version source](./hatch-openapi-version/hatch_openapi_version.py) from openAPI spec
- [metadata source](./hatch_build.py) from openAPI spec; for authors, description and license
- [build hook](./hatch_build.py) producing Python client from the openAPI spec and
  in installation in editable mode creates a dummy README file for the client

-----

**Table of Contents**

- [Installation](#installation)
- [Test](#test)
- [License](#license)

## Installation

```sh
pip install hatch-demo
```

## Test

### Run the server example

1. Run the server

```sh
pip install -e .
python -m hatch_demo
```

2. Test a request

Using [httpie](https://httpie.io/):

```sh
http POST http://localhost:8080/openapi/greeting/john
# or
# curl -X POST http://localhost:8080/openapi/greeting/john
```

You should see:

```
Hello john
```

## License

`hatch-demo` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
