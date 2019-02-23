from .runner import Runner
import database


class StartCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "start_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            return f"Through forbidden black magic named innovation, this is no longer required"
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
