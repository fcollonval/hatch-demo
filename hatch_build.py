import os
from shutil import copyfile, copytree, rmtree, which
from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory
import typing as t

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.metadata.plugin.interface import MetadataHookInterface


class OpenAPIMetadataHook(MetadataHookInterface):
    """The hatch demo metadata hook.

    Read metadata from openAPI specification."""

    # This is ignored because we use it has custom hook
    PLUGIN_NAME = "openapi"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = "src/hatch_demo/spec/openapi.yaml"

    def update(self, metadata: dict) -> None:
        path = os.path.normpath(os.path.join(self.root, self.path))
        if not os.path.isfile(path):
            raise OSError(f"file does not exist: {self.path}")

        with open(path, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)

        info = data["info"]

        if "summary" in info:
            metadata["description"] = info["summary"]

        if "contact" in info:
            contact = info["contact"]
            author = {}
            if "name" in contact:
                author["name"] = contact["name"]
            if "email" in contact:
                author["email"] = contact["email"]
            if len(author):
                metadata["authors"] = [author]

        if "license" in info:
            metadata["license"] = info["license"]["name"]


class JupyterBuildHook(BuildHookInterface):
    """The hatch demo build hook.

    Generate a Python client from the openAPI"""

    PLUGIN_NAME = "openapi"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = "src/hatch_demo/spec/openapi.yaml"
        self.target = "src/hatch_demo/openapi_client"

    def initialize(self, version: str, build_data: dict[str, t.Any]) -> None:
        cmd = which("docker")
        if cmd is None:
            raise ImportError(
                "You need to install docker to generate the Python openapi client."
            )

        if os.path.exists(self.target):
            rmtree(self.target)

        with TemporaryDirectory(delete=False) as tmp_dirname:
            copyfile(self.path, os.path.join(tmp_dirname, "openapi.yaml"))
            uid = os.getuid()
            gid = os.getgid()
            try:
                run(
                    [
                        "docker",
                        "run",
                        "--rm",
                        "--user",
                        f"{uid}:{gid}",
                        "-v",
                        f"{tmp_dirname}:/local",
                        "openapitools/openapi-generator-cli",
                        "generate",
                        "-i",
                        "/local/openapi.yaml",
                        "-g",
                        "python",
                        "-o",
                        "/local/client",
                    ],
                    check=True,
                )
            except CalledProcessError as e:
                print(f"Failed to generate the Python client.\n{e!r}")
                raise e

            copytree(os.path.join(tmp_dirname, "client", "openapi_client"), self.target)

    def finalize(
        self, version: str, build_data: dict[str, t.Any], artifact_path: str
    ) -> None:
        # Available hook
        ...
