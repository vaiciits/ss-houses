import json, os, sys

def load_params():
    f = open(sys.path[0] + os.path.sep + 'params.json', 'r')
    params = json.loads(f.read())
    f.close()
    return params

Params = load_params()