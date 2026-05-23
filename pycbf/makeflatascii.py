
import builtins
def to_str(s):
    if isinstance(s, bytes):
        try: return s.decode("utf-8")
        except: return s.decode("latin-1")
    if isinstance(s, (list, tuple)): return type(s)(to_str(x) for x in s)
    return s
def print(*args, **kwargs):
    builtins.print(*(to_str(a) for a in args), **kwargs)


import pydoc, pycbf, sys
f = open(sys.argv[1],"w")
pydoc.pager=lambda text: f.write(text)
pydoc.TextDoc.bold = lambda self,text : text
pydoc.help(pycbf)
