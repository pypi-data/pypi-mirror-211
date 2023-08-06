""" pytelecontrol """
import toml

try:
    __version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
except Exception:
    __version__ = 'develop'
