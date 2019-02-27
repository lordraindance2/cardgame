class Battle:
    def __init__(self, pk: int, discord_id1, discord_id2, loadout1: list, loadout2: list, bet: int):
        if isinstance(discord_id1, str):
            discord_id1 = int(discord_id1)
        elif isinstance(discord_id2, str):
            discord_id2 = int(discord_id2)

        self._pk = pk
        self._user1 = discord_id1
        self._user2 = discord_id2
        self._loadout1 = loadout1
        self._loadout2 = loadout2
        self._bet = bet

    @property
    def pk(self):
        return self._pk

    @property
    def bet(self):
        return self._bet

    @property
    def user1(self):
        return self._user1

    @property
    def user2(self):
        return self._user2

    @property
    def loadout1(self):
        return self._loadout1

    @property
    def loadout2(self):
        return self._loadout2
