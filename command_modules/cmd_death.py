def command_death(self, command, user):
    if "death_count" not in self.custom_parameters:
        self.custom_parameters['death_count'] = 0
    try:
        count = int("".join(x for x in command if x.isdigit()))
    except ValueError:
        count = 1
    self.custom_parameters["death_count"] += count
    message = "Death Counter: {}".format(
        str(self.custom_parameters["death_count"]))
    self.send_message(self.CHAN, message)
