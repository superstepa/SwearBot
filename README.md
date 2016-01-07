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

#If you need to create a variable, use the self.temp dictionary for temporary variables and self.custom_parameters for persistent ones.
```

The command can then be activated by saying "!COMMANDNAME *args*" in the IRC.

### Config Sample
```json{
  "username": "",
  "admins": [
    ""
  ],
  "host": "irc.twitch.tv",
  "pass": "",
  "port": 6667,
  "channel": "#CHAN"
}
```

### TODO
* Finish the readme
* Redo the config system
* Fix unicode support
* Rewrite the plugin system. Using hardcoded method names for commands? What was I thinking
License
----
MIT
