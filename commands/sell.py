from .runner import Runner
import database
import json
from numbers import Number
from config import get_prefix, set_prefix
import random


class SellCommand(Runner):

    def __init__(self, client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "sell_command"

    def do(self):
        super().do()
        if len(self.args) == 2:
            count = int(self.args[1])
        elif len(self.args) == 1:
            count = 1
        else:
            return f"requires 1 or 2 arguments"
        name = self.args[0]
        card_id = database.get_card(name)
        card = database.get_card_by_id(card_id)
        print(card)
        count = database.sell_card(self.sender, card_id, count)
        if card[3].lower() not in database.money.keys():
            balance = random.random() * 500 + 500
        else:
            balance = database.money[card[3].lower()]
        balance *= count
        if count and database.add_balance(self.sender, balance):
            return f"You removed {count} {self.args[0]} for {balance} money"

