from battlesystem import Battle

battles = []


def add_battle(battle: Battle):
    battles.append(battle)


def remove_battle(battle: Battle):
    if battle in battles:
        battles.remove(battle)


def get_battle(id: int)-> Battle or None:
    first = _get_battle_by_id(id)
    if first is None:
        first = _get_battle_by_user(id)
    return first


def _get_battle_by_id(battle_id: int) -> Battle or None:
    for battle in battles:
        if battle.pk == battle_id:
            return battle
    return None


def _get_battle_by_user(user_id: int)-> Battle or None:
    for battle in battles:
        if battle.user1 == user_id or battle.user2 == user_id:
            return battle
    return None