from .runner import Runner
import database
import json
from numbers import Number
from config import get_prefix, set_prefix


class PrefixCommand(Runner):

    def __init__(self, client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "prefix_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            return f"Current Prefix: {get_prefix(hash(self.message.server))}"
        elif len(self.args) == 1:
            former = get_prefix(hash(self.message.server))
            set_prefix(hash(self.message.server), self.args[0])
            return f"Prefix changed from {former} to {get_prefix(hash(self.message.server))}"
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
