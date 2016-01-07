def command_death(self, command, user):
    if "death_count" not in self.custom_parameters:
        self.custom_parameters["death_count"] = 0
    count = self.get_int_from_msg(command)
    self.custom_parameters["death_count"] += count
    message = "Death Counter: {}".format(
        str(self.custom_parameters["death_count"]))
    self.send_message(self.CHAN, message)


def command_deathcount(self, command, user):
    try:
        count = self.custom_parameters["death_count"]
    except KeyError:
        count = 0
    message = "Death Counter: {}".format(count)
    self.send_message(self.CHAN, message)

def command_setdeath(self, command, user):
    if (self.is_admin(user)):
        count = self.get_int_from_msg(command)
        self.custom_parameters["death_count"] = count
        self.send_message(self.CHAN, "Death counter set to {}".format(count))
