from .runner import Runner
import database
import json
from numbers import Number


class AddCommand(Runner):

    def __init__(self, client, message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "add_command"

    def do(self):
        super().do()
        if int(self.sender.id) != 223212153207783435:
            return f"{self.sender.mention} aren't allowed to do that :D"
        if len(self.args) == 1:
            add_amount = float(self.args[0])
            if database.add_balance(self.sender, add_amount):
                return f"Transaction completed: you added {add_amount} to your moneys"
            else:
                return "forgot to do !start"
        else:
            return f"command {self.name} has too many or too little arguments ( {self.args})"
