from swearbot import SwearCounter
from types import MethodType
from plugin import importModules

main = SwearCounter()
methods = importModules("command_modules")

for method in methods:
    name = method.__name__
    print("Attempting to add the {} command.".format(name))
    try:
        # Creating a command string that is equal to the method name
        main.commands["!"+name.split("_")[1]] = name
        # Appending the method to the main class
        setattr(main, name, MethodType(method, main))
    except IndexError:
        print("Invalid command {}".format(name))

main.run()
