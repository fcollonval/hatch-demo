import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from hatchling.plugin import hookimpl
from hatchling.version.source.plugin.interface import VersionSourceInterface

class OpenAPIVersionSource(VersionSourceInterface):
    PLUGIN_NAME = "openapi"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__path = None

    @property
    def path(self):
        if self.__path is None:
            version_file = self.config.get("path", "openapi.yaml")
            if not isinstance(version_file, (str, bytes, os.PathLike)):
                raise TypeError(
                    "Option `path` for version source `{}` must be a string".format(
                        self.PLUGIN_NAME
                    )
                )

            self.__path = os.fspath(version_file)

        return self.__path

    def get_version_data(self):
        path = os.path.normpath(os.path.join(self.root, self.path))
        if not os.path.isfile(path):
            raise OSError(f"file does not exist: {self.path}")

        with open(path, "r", encoding="utf-8") as f:
            data = load(f, Loader=Loader)

        return {"version": data["info"]["version"]}

    def set_version(self, version: str, version_data):
        path = os.path.normpath(os.path.join(self.root, self.path))
        if not os.path.isfile(path):
            raise OSError(f"file does not exist: {self.path}")

        # Read the original file so we can see if it has a trailing
        # newline character.
        with open(path, "r") as f:
            data = load(f, Loader=Loader)
            
        data["info"]["version"] = version
        with open(path, "w") as f:
            dump(data, f, Dumper=Dumper, sort_keys=False)


@hookimpl
def hatch_register_version_source():
    return OpenAPIVersionSource
