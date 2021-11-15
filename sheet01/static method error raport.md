## TL;DR

Error was caused because prior to python 3.10 functions decorated with `@staticmethod`
were not callable. This was changed in python 3.10 accordingly to the
<a href="https://docs.python.org/3.10/whatsnew/changelog.html#changelog">changelog</a>:

python bug tracking issue that inspired the change: https://bugs.python.org/issue43682

## More elaborate explenation:

I have attempted to do some more digging and from what I understood
there were two main issues in earlier versions of python.
