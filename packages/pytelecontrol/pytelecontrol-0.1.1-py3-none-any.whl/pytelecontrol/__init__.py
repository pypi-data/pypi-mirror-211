""" pytelecontrol """
from importlib import metadata
import toml

try:
    __version__ = metadata.version(__package__)
except Exception:
    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

del metadata  # optional, avoids polluting the results of dir(__package__)
