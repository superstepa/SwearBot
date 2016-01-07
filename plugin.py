import glob
import imp
from os.path import join, basename, splitext


def importModules(dir):
    modules = []
    methods = []

    # Iterating over every file in the directory.
    for path in glob.glob(join(dir, '[!_]*.py')):
        name, ext = splitext(basename(path))
        modules.append(imp.load_source(name, path))

    # Appending all callable methods to the 'methods' list
    for module in modules:
        methods += [f for _, f in module.__dict__.iteritems() if callable(f)]
    return methods
