import socket
import re
import json
import urllib2
import random


class SwearCounter:
    def __init__(self):
        with open("config.json", "r") as cfg:
            CONFIG = json.load(cfg)

        self.HOST = CONFIG['host']
        self.PORT = CONFIG['port']
        self.NICK = CONFIG['username']
        self.PASS = CONFIG['pass']
        self.CHAN = CONFIG['channel']
        self.admins = CONFIG['admins']
        self.debug = CONFIG['debug']
        # Default commands
        self.commands = {"!run": "command_run",
                         "!quit": "command_quit",
                         "!save": "command_save",
                         "!admin": "command_admin",
                         "!help": "command_help"
                         }

        self.isRunning = True
        # Keeps temporary variables accessible by command methods.
        self.temp = {}

        try:
            with open("custom.json") as custom:
                self.custom_parameters = json.load(custom)
        except IOError:
            self.custom_parameters = {}
        except ValueError:
            self.custom_parameters = {}

    def get_int_from_msg(self, msg):
        try:
            count = int("".join(x for x in msg if x.isdigit()))
        except ValueError:
            count = 1
        return count

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
                '''Run the command method if the string is recognized as the
                   command. The arguments are the remainder of the message'''
                getattr(self, self.commands[msg[0]])(msg[1:], sender)

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
                data = data+self.con.recv(1024).decode('utf-8')
                data_split = re.split(r"[~\r\n]+", data)
                data = data_split.pop()

                for line in data_split:
                    line = str.rstrip(str(line.encode('utf-8')))
                    line = str.split(str(line))

                    if len(line) >= 1:
                        if (self.debug):
                            print(' '.join(line))
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

            except KeyboardInterrupt:
                self.command_quit('', self.admins[0])
