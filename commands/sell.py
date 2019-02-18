from .runner import Runner
import database
import json
from numbers import Number
from config import get_prefix, set_prefix


class SellCommand(Runner):

    def __init__(self, client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "sell_command"

    def do(self):
        super().do()
        if len(self.args) == 1:
            name = self.args[0]
            card_id = database.get_card(name)
            card = database.get_card_by_id(card_id)
            print(card)
            if card[3].lower() not in database.money.keys():
                balance = 200
            else:
                balance = database.money[card[3].lower()]
            if database.sell_card(self.sender, card_id) and database.add_balance(self.sender, balance):
                return f"You removed {self.args[0]} for {balance} money"
        else:
            return f"requires 1 argument"
