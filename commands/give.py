from .runner import Runner
import database
import json
from numbers import Number


class GiveCommand(Runner):

    def __init__(self, client, message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "add_command"

    def do(self):
        super().do()
        if int(self.sender.id) != 223212153207783435:
            return f"{self.sender.mention} aren't allowed to do that :D"
        if len(self.args) == 1:
            card_id = int(self.args[0])
            if database.add_card(self.sender, card_id):
                return f"Transaction completed: you added {database.get_card_by_id(card_id)} to your cards"
            else:
                return "forgot to do !start"
        else:
            return f"command {self.name} has too many or too little arguments ( {self.args})"
