import oyaml as yaml
import os


def load(filename, throw=False):
    if filename and os.path.isfile(filename):
        with open(filename) as f:
            return yaml.safe_load(f)
    elif throw:
        raise Exception(f"didn't find file: {filename}")
