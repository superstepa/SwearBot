import datetime


def command_time(self, command, user):
    self.send_message(
     self.CHAN,
     datetime.datetime.now().strftime("%d-%B-%Y %H:%M%p")
     )
