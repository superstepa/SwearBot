from swearbot import SwearCounter
from types import MethodType
from plugin import importModules

main = SwearCounter()
methods = importModules("command_modules")
for method in methods:
    name = method.__name__
    print("Attempting to add the {} command.".format(name))
    main.commands["!"+name.split("_")[1]] = name
    setattr(main, name, MethodType(method, main))

main.run()
