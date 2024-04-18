"""Hello world example from connexion.

Licensed under Apache-2.0 license
"""

from pathlib import Path

import connexion


async def test():
    pass


async def post_greeting(name: str):
    await test()
    return f"Hello {name}", 201


app = connexion.AsyncApp(__name__, specification_dir="spec")
app.add_api("openapi.yaml", arguments={"title": "Hello World Example"})


def main():
    app.run(f"hatch_demo.{Path(__file__).stem}:app", port=8080)
