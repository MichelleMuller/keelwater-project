import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name, relative_path):
    """Import a script from the repo by path (the folders aren't Python packages)."""
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
