from importlib import import_module

__all__ = [
    "import_from_string",
]


def import_from_string(dot_path: str) -> object:
    module_path, _, name = dot_path.rpartition(".")
    module = import_module(module_path)
    return getattr(module, name)
