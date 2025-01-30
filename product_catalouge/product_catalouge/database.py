import sys
from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import Iterator

from beanie import Document


FILE_PATH = Path(__file__)

APP_DIR = FILE_PATH.parent


def is_beanie_model(item) -> bool:
    """Determines if item is a Beanie Document object."""
    return (isclass(item) and issubclass(item, Document) )


def get_modules(modules_dirname) -> Iterator[str]:
    """Returns all .py modules in given file_dir as
    a generator of dot separated string values.
    """
    modules_dir_path = Path(APP_DIR/modules_dirname)
    print(f"[MODULES DIR PATH]: {modules_dir_path}")
    module_parent_idx_end = len(APP_DIR.parts) - 1
    modules = [f for f in list(modules_dir_path.rglob("*.py")) 
                if f.stem != "__init__"]
    for filepath in modules:
        yield (".".join(filepath.parts[module_parent_idx_end+1:])[0:-3])


def dynamic_loader(modules_dirname, compare) -> list:
    """Iterates over all .py files in `module` directory,
    finding all classes that match `compare` function.
    """
    items = []
    for mod in get_modules(modules_dirname):
        print(f"[MODULE PATH]: {mod}")
        print("*"*60, "\n")
        module = import_module(mod)
        if hasattr(module, "__all__"):
            objs = ([getattr(module, obj)
                    for obj in module.__all__])
            items += [o for o in objs
                    if compare(o) and o not in items]
    return items


def get_beanie_models() -> list[str]:
    """Dynamic Beanie model finder."""
    sys.path.append(APP_DIR)
    return dynamic_loader("product_catalouge.models", is_beanie_model)



if __name__ == "__main__":
    print(f"[APP DIR PATH]: {APP_DIR}")
    print(f"[CWD]: {Path.cwd()}")
    sys.path.append(APP_DIR.parent)
    print(dynamic_loader("models", is_beanie_model))
    # print(list(get_modules('models')))