import os
import typing as t

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from hatchling.metadata.plugin.interface import MetadataHookInterface


class OpenAPIMetadataHook(MetadataHookInterface):
    """The hatch demo metadata hook."""

    # This is ignored because we use it has custom hook
    PLUGIN_NAME = 'openapi'

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


class JupyterBuildHook(BuildHookInterface[JupyterBuildConfig]):
    """The hatch demo build hook."""

    PLUGIN_NAME = "openapi"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.path = "src/hatch_demo/spec/openapi.yaml"

    def initialize(self, version: str, build_data: dict[str, t.Any]) -> None:
        ...

    def finalize(self, version: str, build_data: dict[str, t.Any], artifact_path: str) -> None:
        ...