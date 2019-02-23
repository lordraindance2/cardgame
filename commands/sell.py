from .runner import Runner
import database
import random


class SellCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "sell_command"

    def do(self):
        super().do()
        _isList = False
        count = 1
        if len(self.args) == 2:
            try:
                count = int(self.args[1])
            except ValueError:
                _isList = True
        elif len(self.args) == 1:
            count = 1
        else:
            return f"requires 1 or 2 arguments"

        name = self.args[0]
        if len(self.args) > 1 and _isList:
            name = self.args[0:]
        if name == "ALL":
            cards = database.get_cards(self.sender)
            cards_ = database.get_card_by_ids(cards)
            b = 0
            for card in cards_:
                count = database.sell_card(self.sender, card[1])
                if count != 0:
                    if card[3].lower() not in database.money.keys():
                        balance = int(random.random() * 500 + 500)
                    else:
                        balance = database.money[card[3].lower()]
                    b += balance
            if database.add_balance(self.sender, b):
                return f"You sold everything for {b} money"
        else:
            a = ""
            if isinstance(name, str):
                a = self.sell(name, count)
            elif isinstance(name, list):
                b = []
                for n in name:
                    b.append(self.sell(n, 1))
                a = "\n".join(b)
            return a

    def sell(self, name, count):
        print(name)
        card_id = database.get_card(name)
        card = database.get_card_by_id(card_id)
        count = database.sell_card(self.sender, card_id, count)
        if card[3].lower() not in database.money.keys():
            balance = int(random.random() * 500 + 500)
        else:
            balance = database.money[card[3].lower()]
        balance *= count
        if count and database.add_balance(self.sender, balance):
            return f"You removed {count} {card[2]} for {balance} money"
