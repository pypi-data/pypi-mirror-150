findfile_path
=============

Find the first instance of a file on a path of directories, with
possible file extensions.

::

  findfile_path (fname, path, exts = None)

fname can be either a string or Path object, or an iterable of strings
or Path objects.  The first matching file in the first directory on
path (a list of string or Path objects) with the first extension (exts
-- an optional list of strings) is returned, else None.
