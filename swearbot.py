import socket
import re
import json
import urllib2
import random

'''
TODO:
COMPLETELY MOVE ALL REFERNCES TO EXTERNAL FUNCTIONS OUT OF THE MAIN CLASS
'''

with open("config.json") as cfg:
    CONFIG = json.load(cfg)


class SwearCounter:
    def __init__(self):
        self.HOST = CONFIG['host']
        self.PORT = CONFIG['port']
        self.NICK = CONFIG['username']
        self.PASS = CONFIG['pass']
        self.CHAN = CONFIG['channel']
        self.bad_words = CONFIG['bad_words']
        self.swearcount = CONFIG['swearcount']
        self.admins = CONFIG['admins']

        self.commands = {'!ping': "command_pong",
                         "!run": "command_run",
                         "!debug": "command_debug",
                         "!swear": "command_swear",
                         "!quit": "command_quit",
                         "!save": "command_save",
                         "!new_word": "command_words",
                         "!admin": "command_admin",
                         "!help": "command_help"
                         }

        self.debug = False
        self.isRunning = True

        self.playing_hangman = False
        self.hangman_lives = 5
        self.hangman_word = ""
        self.hangman_guess = []

    def send_pong(self, msg):
        self.con.send(bytes('PONG {}\r\n'.format(msg)))

    def send_message(self, chan, msg):
        self.con.send(bytes('PRIVMSG {0} :{1}\r\n'.format(chan, msg))
                      .encode('UTF-8'))

    def send_nick(self, nick):
        self.con.send(bytes('NICK {}\r\n'.format(nick)))

    def send_pass(self, password):
        self.con.send(bytes('PASS {}\r\n'.format(password)))

    def join_channel(self, chan):
        print("Successfully joined {}".format(chan))
        self.con.send(bytes('JOIN {}\r\n'.format(chan)))

    def part_channel(self, chan):
        self.con.send(bytes('PART {}\r\n'.format(chan)))

    def is_admin(self, user):
        return user in self.admins

    def get_sender(self, msg):
        result = ""
        for char in msg:
            if char == "!":
                break
            if char != ":":
                result += char
        return result

    def get_message(self, msg):
        result = ""
        i = 3
        length = len(msg)
        while i < length:
            result += msg[i] + " "
            i += 1
        result = result.lstrip(':')
        return result

    def parse_message(self, sender, msg):
        if len(msg) >= 1:
            msg = msg.split(' ')
            if (msg[0] in self.commands):
                getattr(self, self.commands[msg[0]])(msg[1:], sender)
            for word in msg:
                if word in self.bad_words:
                    print("Swear word detected: {}".format(word))
                    self.swearcount += 1
                    self.announce_swearcount()

    def announce_swearcount(self):
        message = "Swear Counter: {}".format(str(self.swearcount))
        self.send_message(self.CHAN, message)

    def command_pong(self, command, user):
        self.send_message(self.CHAN, "Pong")

    def command_run(self, command, user):
        if self.is_admin(user):
            command = " ".join(command)
            print(command)
            self.con.send(bytes('{}\r\n'.format(command)))
        else:
            self.send_message(self.CHAN, "Sorry bub.")

    def command_debug(self, command, user):
        if (self.is_admin(user)):
            states = ["ON", "OFF"]
            self.debug = not self.debug
            print("DEBUG MODE {}".format(states[self.debug]))

    def command_swear(self, command, user):
        if (self.is_admin(user)):
            count = int("".join(x for x in command if x.isdigit()))
            self.swearcount += count
            self.announce_swearcount()

    def command_quit(self, command, user):
        if (self.is_admin(user)):
            self.send_message(self.CHAN, "Shutting down")
            self.command_save(command, user)
            self.isRunning = False

    def command_save(self, command, user):
        if (self.is_admin(user)):
            with open("config.json", "r+") as cfg:
                CONFIG = json.load(cfg)
                CONFIG['swearcount'] = self.swearcount
                CONFIG['admins'] = list(set(self.admins))
                CONFIG['bad_words'] = list(set(self.bad_words))
                cfg.seek(0)
                cfg.write(json.dumps(CONFIG))
                cfg.truncate()
                print("Saved successfully.")

    def command_words(self, command, user):
        if (self.is_admin(user)):
            command = " ".join(command)
            self.bad_words.append(command)
            self.send_message(
                        self.CHAN,
                        "Added {} to the list of swear words".format(command)
                              )

    def command_admin(self, command, user):
        if (self.is_admin(user)):
            command = " ".join(command)
            self.admins.append(command)
            self.send_message(self.CHAN,
                              "Added {} to the admin list".format(command))

    def command_help(self, command, user):
        keys = [i for i in self.commands.keys()]

        msg = "Avaliable commands are:{}. Most commands are admin only".format(
         ", ".join(x for x in keys))
        self.send_message(self.CHAN, msg)

    def run(self):
        self.con = socket.socket()
        self.con.connect((self.HOST, self.PORT))

        self.send_pass(self.PASS)
        self.send_nick(self.NICK)
        self.join_channel(self.CHAN)
        self.send_message(self.CHAN, "Hi.")
        data = ""

        while self.isRunning:
            try:
                data = data+self.con.recv(1024).decode('UTF-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()

                for line in data_split:
                    line = str.rstrip(str(line))
                    line = str.split(str(line))

                    if len(line) >= 1:
                        if (self.debug):
                            print(line)
                        if line[0] == 'PING':
                            self.send_pong(line[1])

                        elif line[1] == 'PRIVMSG':
                            sender = self.get_sender(line[0])
                            message = self.get_message(line)
                            self.parse_message(sender, message)
                            print(sender + ": " + message)

            except socket.error:
                print("Socket died")

            except socket.timeout:
                print("Socket timeout")
