from .runner import Runner
import database
import json
from numbers import Number


class BalanceCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, ..., message, sender, args)
        self.name = "balance_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            balance = database.get_balance(self.sender)
            if balance or isinstance(balance, Number):
                return f"You have {balance} moneys"
            else:
                return "forgot to do !start"
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
