import os
import importlib
import glob

all_module = []
all_method = set()

all_module = [os.path.basename(x) for x in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"),recursive=True)]
all_module = [module[:-3] for module in all_module if module != "__init__.py"]
for module in all_module:
    exec(f'{module} = importlib.import_module(__package__ + "." + module)')
    # me = [method for method in dir(module) if method.startswith('__') is False]
    # all_method.update(me)
    # for x in me:
    #     globals()[x] = getattr(module, x)

# __all__ = list(all_method)
