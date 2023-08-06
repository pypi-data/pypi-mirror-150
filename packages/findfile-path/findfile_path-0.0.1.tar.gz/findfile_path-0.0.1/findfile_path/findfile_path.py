#! /usr/bin/env python

import logtool
from path import Path

@logtool.log_call
def findfile_path (fname, path, exts = None):
  for d in path:
    d = Path (d)
    print (d / fname)
    if (d / fname).isfile ():
      return (d / fname).strip ()
    if exts:
      for e in exts:
        print (d / fname + e)
        if (d / fname + e).isfile ():
          return (d / fname + e).strip ()
  raise ValueError ("No matching file found")
