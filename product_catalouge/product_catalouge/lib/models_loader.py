import sys
from importlib import import_module
from inspect import isclass
from pathlib import Path
from typing import Iterator

from beanie import Document


FILE_PATH = Path(__file__)
APP_DIR = FILE_PATH.parent.parent
sys.path.insert(0, str(APP_DIR))


def is_beanie_model(item) -> bool:
    """Determines if item is a Beanie Document object."""
    return (isclass(item) and issubclass(item, Document) )


def get_modules(modules_dirname) -> Iterator[str]:
    """Returns all .py modules in given file_dir as
    a generator of dot separated string values.
    """
    modules_dir_path = Path(APP_DIR/modules_dirname)
    # print(f"[MODULES DIR PATH]: {modules_dir_path}")
    module_idx = len(APP_DIR.parts)
    modules = [f for f in list(modules_dir_path.rglob("*.py")) 
                if f.stem != "__init__"]
    for filepath in modules:
        yield (".".join(filepath.parts[module_idx:])[0:-3])


def dynamic_loader(modules_dirname, compare) -> list:
    """Iterates over all .py files in `module` directory,
    finding all classes that match `compare` function.
    """
    items = []
    for mod in get_modules(modules_dirname):
        # print(f"[MODULE PATH]: {mod}")
        # print("*"*60, "\n")
        module = import_module(mod)
        if hasattr(module, "__all__"):
            objs = ([getattr(module, obj)
                    for obj in module.__all__])
            items += [o for o in objs
                    if compare(o) and o not in items]
    return items


def get_beanie_models() -> list[str]:
    """Dynamic Beanie model finder."""
    return dynamic_loader("models", is_beanie_model)



if __name__ == "__main__":
    print(f"[APP DIR PATH]: {APP_DIR}")
    print(f"[CWD]: {Path.cwd()}")
    print(f"[ROOT]: {str(APP_DIR)}")
    print(get_beanie_models())