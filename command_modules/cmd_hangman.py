from random import choice
import os
'''
This is really messy at the moment, needs to be completely changed.
'''


def command_hangman(self, command, user):
    if 'is_playing' not in self.temp:
        self.temp['is_playing'] = False
        self.temp['lives'] = 5
        self.temp['word'] = ""
        self.temp['guess'] = []

    if not self.temp['is_playing']:
        self.temp['is_playing'] = True
        valid = "abcdefghijklmnopqrstuvwxyz"

        with open(
          os.path.join(os.path.dirname(__file__),
                       '../data/wordsEn.txt')) as f:
                        l = f.read().splitlines()

        self.temp['word'] = choice(l).strip()

        self.temp['word'] = ''.join(
           char for char in self.temp['word'] if char in valid)

        lng = len(self.temp['word'])
        self.temp['lives'] = lng
        self.temp['guess'] = ["*"]*lng
        self.send_message(self.CHAN, "A new game of hangman has started.\
        The word has {} letters.".format(lng))

        if (self.debug):
            print("The word is {}".format(self.temp['word']))
    else:
        try:
            command = "".join(command)[0]
        except IndexError:
            return
        if command in self.temp['word']:
            for x in range(0, len(self.temp['word'])):
                if command == self.temp['word'][x]:
                    self.temp['guess'][x] = command

            if ('*' not in self.temp['guess']):
                msg = "You won with {} lives left out of {}!".format(
                    self.temp['lives'], len(self.temp['word']))

                self.temp['is_playing'] = False
            else:
                msg = ''.join(x for x in self.temp['guess'])
        else:
            if (self.temp['lives'] > 1):
                self.temp['lives'] -= 1
                msg = "You have {} lives left".format(self.temp['lives'])
            else:
                msg = "You lose. The word was {}".format(self.temp['word'])
                self.temp['is_playing'] = False
        self.send_message(self.CHAN, msg)
