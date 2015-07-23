# Swearbot
Swearbot is a simple IRC bot developed in pure python.

### Features
* No external libraries need
* Extendable using plugins

### Plugin development
Any python file placed into the "command_directories" (default name) directory will be automatically loaded. For the methods to be properly recognized by the bot they need to follow the following template:

```python

def command_COMMANDNAME(self, arg, user):
    pass
#self is the main class, arg is the arguments sent by the user and user is the username
```

The command can then be activated by saying "!COMMANDNAME *args*" in the IRC.
### TODO
* Finish the readme
* Redo the config system
* Move unnecessary functions from the base class to modules.
* Remove the swear word detector or move it to modules. This project is what happens when you get way too attached to a joke, it's time to let it go. 

License
----
MIT
