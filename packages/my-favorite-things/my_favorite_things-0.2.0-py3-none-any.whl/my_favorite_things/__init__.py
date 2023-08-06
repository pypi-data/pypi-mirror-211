from importlib.metadata import version

from .save import save
from .ddicts import nested_ddict, format_ddict

__all__ = ["save", "nested_ddict", "format_ddict"]
__version__ = version("my-favorite-things")
