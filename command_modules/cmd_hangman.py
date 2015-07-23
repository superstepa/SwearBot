import urllib2


def command_hangman(self, command, user):
    if "playing_hangman" not in self.custom_parameters:
        self.custom_parameters["playing_hangman"] = False
        self.custom_parameters["hangman_lives"] = 5
        self.custom_parameters["hangman_word"] = ""
        self.custom_parameters["hangman_guess"] = []

    is_playing = self.custom_parameters["playing_hangman"]
    lives = self.custom_parameters["hangman_lives"]
    word = self.custom_parameters["hangman_word"]
    guess = self.custom_parameters["hangman_guess"]

    if not is_playing:
        is_playing = True
        valid = "abcdefghijklmnopqrstuvwxyz"
        word = urllib2.urlopen(
            "http://randomword.setgetgo.com/get.php").read()
        word = ''.join(
           char for char in word if char in valid)
        lng = len(word)
        lives = lng
        guess = ["*"]*lng
        self.send_message(self.CHAN, "A new game of hangman has started.\
        The word has {} letters.".format(lng))
        if (self.debug):
            print("The word is {}".format(word))
    else:
        command = "".join(command)[0]
        if command in word:
            for x in range(0, len(word)):
                if command == word[x]:
                    word[x] = command
            if ('*' not in guess):
                msg = "You won with {} lives left out of {}!".format(
                    lives, len(word))
                is_playing = False
            else:
                msg = ''.join(x for x in guess)
        else:
            if (lives > 1):
                lives -= 1
                msg = "You have {} lives left".format(lives)
            else:
                msg = "You lose. The word was {}".format(word)
                self.is_playing = False
        self.send_message(self.CHAN, msg)
