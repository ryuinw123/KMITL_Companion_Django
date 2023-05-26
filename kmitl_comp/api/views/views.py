import os
import importlib
import glob

modpath = [os.path.basename(x) for x in glob.glob(os.path.join(os.path.dirname(__file__), "views_methods/**"))]
modpath = [".views_methods."+path for path in modpath if path not in ["__init__.py","__pycache__"]]
modnames = modpath

for lib in modnames:
    #globals()[lib] = importlib.import_module(lib,package=__package__)
    exec(f'{lib.split(".")[-1]} = importlib.import_module(__package__ + lib)')
    # for symbol in module.__all__:
    #     globals()[symbol] = getattr(module, symbol)
