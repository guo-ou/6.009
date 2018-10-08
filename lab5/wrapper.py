import json, traceback, time
import lab
from importlib import reload
reload(lab)  # this forces the student code to be reloaded when page is refreshed

import os
import importlib, importlib.util
from collections import OrderedDict

# These functions are required by the UI
def ui_list_db_names(d):
    return list(dbs.keys())

def ui_list_dbs(d):
    return dbs

def ui_assign(d):
    return lab.managers_for_actors(d["K"], dbs[d["db_name"]])



# State that is used by the ui
dbs = None

## Initialization
def init():
    global dbs
    dbs = OrderedDict()
    for i in os.listdir('resources/db'):
        if not i.endswith('.json'):
            continue

        x = i.rsplit('.', 1)[0]

        with open('./resources/db/%s.json' % x, 'r') as f:
            js = json.load(f)
            dbs[x] = js

init()
