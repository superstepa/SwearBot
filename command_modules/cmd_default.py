import json


def command_run(self, command, user):
    if self.is_admin(user):
        command = " ".join(command)
        print(command)
        self.con.send(bytes('{}\r\n'.format(command)))
    else:
        self.send_message(self.CHAN, "Sorry bub.")


def command_quit(self, command, user):
    if (self.is_admin(user)):
        self.send_message(self.CHAN, "Shutting down")
        self.command_save(command, user)
        self.isRunning = False


def command_save(self, command, user):
    if (self.is_admin(user)):
        with open("config.json", "r+") as cfg:
            CONFIG = json.load(cfg)
            CONFIG['admins'] = list(set(self.admins))
            cfg.seek(0)
            cfg.write(json.dumps(CONFIG))
            cfg.truncate()
            print("Saved the main config successfully.")

        with open("custom.json", "w") as custom:
            custom.write(json.dumps(self.custom_parameters))
            print("Saved the custom attributes successfully.")


def command_admin(self, command, user):
    if (self.is_admin(user)):
        command = " ".join(command)
        self.admins.append(command)
        self.send_message(self.CHAN,
                          "Added {} to the admin list".format(command))


def command_help(self, command, user):
    keys = [i for i in self.commands.keys()]

    msg = "Avaliable commands are: {}. Some are admin only".format(
     ", ".join(x for x in keys))

    self.send_message(self.CHAN, msg)
