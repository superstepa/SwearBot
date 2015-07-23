from random import getrandbits


def command_coin(self, command, user):
    self.send_message(
     self.CHAN,
     ['Heads', 'Tails'][getrandbits(1)]
     )
