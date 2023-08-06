#! /usr/bin/env python

import logtool
from path import Path
from collections.abc import Iterable

@logtool.log_call
def findfile_path (fname, path, exts = None):
  if not isinstance (fname, Iterable):
    fnames = [fname,]
  else:
    fnames = fname
  for d in path:
    for f in fnames:
      d = Path (d).expanduser ()
      if exts is None and (d / f).isfile ():
        return (d / f).strip ()
      if exts:
        for e in exts:
          if (d / f + e).isfile ():
            return (d / f + e).strip ()
  return None
