class LoadOut:
    def __init__(self, pk: int, discord_id, cards: list):
        if isinstance(discord_id, str):
            discord_id = int(discord_id)
        self._pk = pk
        self._discord_id = discord_id
        self._cards = cards
        if len(self.cards) > 5:
            self._cards = []
            raise ValueError("Too many cards, must only be 5")

    @property
    def pk(self):
        return self._pk

    @property
    def user_id(self):
        return self._discord_id

    @property
    def cards(self):
        return self._cards
