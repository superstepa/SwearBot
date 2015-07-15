import urllib2
import json
import random


def command_aww(self, command, user):
    hdr = {'User-Agent': 'Grabbing an awwducational post by /u/superstepa'}
    url = "http://www.reddit.com/r/awwducational/new.json"
    req = urllib2.Request(url, headers=hdr)
    response = urllib2.urlopen(req).read()
    data = json.loads(response)
    post = random.choice(data['data']['children'])
    title = post['data']['title'].encode('utf-8')
    self.send_message(self.CHAN, title)


def command_hangman(self, command, user):
    if not self.playing_hangman:
        self.playing_hangman = True
        valid = "abcdefghijklmnopqrstuvwxyz"
        self.hangman_word = urllib2.urlopen(
            "http://randomword.setgetgo.com/get.php").read()
        self.hangman_word = ''.join(
           char for char in self.hangman_word if char in valid)
        lng = len(self.hangman_word)
        self.hangman_lives = lng
        self.hangman_guess = ["*"]*lng
        self.send_message(self.CHAN, "A new game of hangman has started.\
        The word has {} letters.".format(lng))
        if (self.debug):
            print("The word is {}".format(self.hangman_word))
    else:
        command = "".join(command)
        command = command[0]
        if command in self.hangman_word:
            for x in range(0, len(self.hangman_word)):
                if command == self.hangman_word[x]:
                    self.hangman_guess[x] = command
            if ('*' not in self.hangman_guess):
                msg = "You won with {} lives left out of {}!".format(
                    self.hangman_lives, len(self.hangman_word))
                self.playing_hangman = False
            else:
                msg = ''.join(x for x in self.hangman_guess)
        else:
            if (self.hangman_lives > 1):
                self.hangman_lives -= 1
                msg = "You have {} lives left".format(self.hangman_lives)
            else:
                msg = "You lose. The word was {}".format(self.hangman_word)
                self.playing_hangman = False
        self.send_message(self.CHAN, msg)
