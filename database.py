import sqlite3
from discord import Client
import json
import pandas as pd
import util
from typing import Tuple
import random
import ast
import numpy as np


connect = sqlite3.connect("sql.db")
# connect = sqlite3.connect(":memory:")
c = connect.cursor()

valid_types = ["common", "uncommon", "rare", "mythic", "legendary", "iconic"]
money = {
    "common": 1,
    "uncommon": 7,
    "rare": 12,
    "mythic": 18,
    "iconic": 26
}
packs = {
    "wood": {
        "cost": 25,
        "rarity": {
            "common": 0.0,  # 50%
            "uncommon": 0.7,  # 30%
            "rare": 0.9,  # 10%
            "mythic": 0.95,  # 0.5%
            "legendary": 0.97,  # 0.4%
            "iconic": 0.99  # 0.1%
        }
    },
    "iron": {
        "cost": 75,
        "rarity": {
            "common": 0.0,
            "uncommon": 0.4,
            "rare": 0.8,
            "mythic": 0.85,
            "legendary": 0.9,
            "iconic": 0.95
        }
    },
    "gold": {
        "cost": 150,
        "rarity": {
            "common": 0.0,
            "uncommon": 0.3,
            "rare": 0.7,
            "mythic": 0.8,
            "legendary": 0.9,
            "iconic": 0.95
        }
    },
}


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS cards(indexer INTEGER PRIMARY KEY, name TEXT, typeo TEXT, class TEXT);")
    import_cards()
    c.execute("CREATE TABLE IF NOT EXISTS users(primary_key INTEGER PRIMARY KEY, balance INTEGER, card_ids BLOB);")
    #c.execute("DELETE FROM users WHERE primary_key = 223212153207783435;")
    connect.commit()


def import_cards():
    cards_csv = pd.read_csv("cards.csv")
    cards_csv.insert(0, "indexer", range(0, len(cards_csv)))
    cards_csv.to_sql("cards", connect, if_exists="replace")


def show_table():
    c.execute("PRAGMA table_info('cards')")
    print(c.fetchall())
    c.execute("SELECT * FROM cards")
    return c.fetchall()


def init_user(user):
    """
    :param user: Discord user
    :return:
    """
    if get_user(user.id) is None:
        new_data = (user.id, 0, json.dumps([]))
        c.execute("INSERT INTO users VALUES (?, ?, ?);", new_data)
        connect.commit()
        return True
    else:
        print(f"This user {user.name} has already been inited")
    return False


def get_user(key: int):
    search = (key, )
    c.execute("SELECT * FROM users WHERE primary_key=?;", search)
    return c.fetchone()


def get_balance(user):
    id = get_user(user.id)
    if id is not None:
        c.execute("SELECT balance FROM users WHERE primary_key=?;", (user.id, ))
        result = c.fetchone()
        return result[0]
    else:
        print(f"This user {user.name} has not initialized")
    return False


def set_balance(user, balance):
    id = get_user(user.id)
    if id is not None:
        c.execute("UPDATE users SET balance= ? WHERE primary_key=?;", (balance, user.id))
        connect.commit()
        return True
    else:
        print(f"This user {user.name} has not initialized")
    return False


def add_balance(user, balance):
    id = get_user(user.id)
    if id is not None:
        c.execute("UPDATE users SET balance= ? WHERE primary_key=?;", (get_balance(user) + balance, user.id))
        connect.commit()
        return True
    else:
        print(f"This user {user.name} has not initialized")
    return False


def add_card(user, card_id):
    if isinstance(card_id, list) or isinstance(card_id, tuple):
        add_cards(user, card_id)
        return
    else:
        id = get_user(user.id)
        card = get_card_by_id(card_id)
        if id is not None and card is not None:
            cards = get_cards(user)
            if cards is None:
                cards = []
            cards.append(card_id)
            a = json.dumps(cards)
            c.execute("UPDATE users SET card_ids= ? WHERE primary_key=?;", (a, user.id))
            connect.commit()
            return True
        else:
            print(f"This user {user.name} has not initialized")
        return False


def sell_card(user, card_id: int):
    if get_user(user.id) is not None or get_card_by_id(card_id) is not None:
        cards = get_cards(user)
        print(cards)
        print(type(cards[0]))
        cards.remove(card_id)
        c.execute("UPDATE users SET card_ids= ? WHERE primary_key=?;", (json.dumps(cards), user.id))
        connect.commit()
        return True
    else:
        return False


def add_cards(user, card_ids):
    id = get_user(user.id)
    card = get_card_by_id(card_ids[0])
    if id is not None and card is not None:
        cards = get_cards(user)
        if cards is None:
            cards = []
        cards.extend(card_ids)
        a = json.dumps(cards)
        c.execute("UPDATE users SET card_ids= ? WHERE primary_key=?;", (a, user.id))
        connect.commit()
        return True
    else:
        print(f"This user {user.name} has not initialized")
    return False


def get_card_by_id(card_id):
    c.execute("SELECT * "
              "FROM cards "
              "WHERE indexer=?;", (card_id, ))
    result = c.fetchone()
    return result


def get_card_by_ids(card_ids):
    print(type(card_ids))
    a = []
    for cc in card_ids:
        print(cc)
        c.execute("SELECT * FROM cards WHERE indexer = ?;", (cc, ))
        a.append(c.fetchone())
    df = pd.DataFrame(a, columns=["row", "indexer", "name", "typeo", "class"]).sort_values(["typeo"])
    return df["indexer"].tolist()


def all_cards(page: int, limit: int = 10, type_: str = "*"):
    if limit == -1:
        limit = count_all_cards()
    if type_ == "*":
        c.execute("SELECT * FROM cards LIMIT ? OFFSET ?;", (limit, limit * page,))
    else:
        c.execute("SELECT * FROM cards WHERE typeo=? LIMIT ?, ?;", (type_, page, limit,))
    return c.fetchall()


def count_all_cards() -> int:
    c.execute("SELECT COUNT (*) FROM cards")
    return c.fetchone()[0]


def get_card(name: str) -> int:
    c.execute("SELECT indexer FROM CARDS WHERE name = ? LIMIT 1;", (name, ))
    return c.fetchone()[0]


def get_cards(user):
    if get_user(user.id) is not None:
        c.execute("SELECT card_ids "
                  "FROM users "
                  "WHERE primary_key=?;", (user.id, ))
        cards = c.fetchone()
        print(cards)
        cards = ast.literal_eval(cards[0])
        if not cards:
            cards = []
        # else:
        #   cardss = [get_card_by_id(int(c)) for c in cards]
        print(cards)
        cards = [int(k) for k in cards]
        a = get_card_by_ids(cards)
        print(a)
        return a
    else:
        print(f"This user {user.name} has not initialized")
        return False


def buy_pack(user, pack: str):
    if get_user(user.id) is None:
        print(f"This user {user.name} has not initialized")
        return False
    elif get_balance(user) - packs[pack]["cost"] < 0:
        print(f"This user is in debt")
    else:
        add_balance(user, -packs[pack]["cost"])
        temp = valid_types
        a = []
        for i in range(7):
            guesser = random.random()
            last = ""
            for valid_type in temp:
                probability = packs[pack]["rarity"][valid_type]
                if guesser >= probability:
                    last = valid_type
            possible = all_cards(0, -1, last.capitalize())
            a.append(possible[random.randint(0, len(possible)-1)])
        d = np.array(a)
        add_card(user, d[:, 1].tolist())
        return a
