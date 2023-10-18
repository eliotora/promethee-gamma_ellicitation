import json
from pathlib import Path


def load_dataset(filename, folder=None):
    """Author: Gilles Dejaegere"""
    if folder is None:
        folder = Path(__file__).parent / ".."

    s = open(folder / (filename + ".json"), "r").read()
    d = json.loads(s)
    return d['alternatives'], d['weights'], d['preference_fct_descriptions']

if __name__ == "__main__":
    A, w, pref_fct_desc = load_dataset("data/HDI20_Classic")
    print(A)
