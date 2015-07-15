from swearbot import SwearCounter
from types import MethodType
from commands import command_hangman, command_aww

main = SwearCounter()

main.commands["!hangman"] = command_hangman.__name__
main.command_hangman = MethodType(command_hangman, main)

main.commands["!aww"] = command_aww.__name__
main.command_aww = MethodType(command_aww, main)

main.run()

'''
import commands as foo
[f for _, f in foo.__dict__.iteritems() if callable(f)]
http://tmi.twitch.tv/group/user/superstepa/chatters
'''
