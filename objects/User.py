
class User(object):
    def __init__(self, pk, discord_id, cards, balance):
        self.pk = pk
        self.cards = cards
        self.discord_id = discord_id
        self.balance = balance

    @property
    def primary_key(self):
        return self.pk

    @property
    def cards(self):
        return self.cards

    @property
    def balance(self):
        return self.balance

    @cards.setter
    def cards(self, cards):
        self.cards = cards

    @balance.setter
    def balance(self, balance):
        self.balance = balance
