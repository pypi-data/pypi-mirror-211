

import json
import pickle
from pathlib import Path


def make_parent_dir(fpath):
    dir_ = Path(fpath).parent
    if not dir_.exists():
        dir_.mkdir()

def save_pickle(fpath: str,
                data: dict,
                make_dir: bool = False):
    if make_dir:
        make_parent_dir(fpath)
    with open(fpath, 'wb') as obj:
        pickle.dump(data, obj, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(fpath: str) -> dict:
    with open(fpath, 'rb') as obj:
        return pickle.load(obj)

def save_json(fpath: str,
              obj: dict,
              make_dir: bool = False):
    if make_dir:
        make_parent_dir(fpath)
    with open(fpath, 'w') as fp:
        json.dump(obj, fp, sort_keys=True, indent=4)

def load_json(fpath: str) -> dict:
    with open(fpath, 'r') as fp:
        return json.load(fp)