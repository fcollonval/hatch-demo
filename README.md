# Hatch Demo

This is a demonstrator for hatch hooks presented at Python Rennes Meetup 04-2024.

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
hatch shell
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
