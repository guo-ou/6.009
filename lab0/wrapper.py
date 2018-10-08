import lab, json
from importlib import reload
reload(lab) # this forces the student code to be reloaded when page is refreshed

def init():
  p = False
  # We don't need to init anything, but we do need to have something here
  # else python complains. 

def next( d ):
  r = None
  # MUX
  r = lab.step(d["gas"])
  return r

init()
