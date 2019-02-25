import sqlite3
import json
import pandas as pd
import util
from typing import Tuple
import random
import ast
import numpy as np
from collections import Counter
from decimal import *


getcontext().prec = 2
connect = sqlite3.connect("sql.db")
# connect = sqlite3.connect(":memory:")
c = connect.cursor()

valid_types = ["common", "uncommon", "rare", "mythic", "legendary", "iconic"]

default_prefix = "$"

command_alias = [
    (["auct", "auctions", "a", "auction"], "auction"),
    (["b", "bal", "balance"], "balance"),
    (["buypack", "buy"], "buy"),
    (["c", "cs", "cards"], "cards"),
    (["clist", "cardslist"], "cardslist"),
    (["g", "gamble"], "gamble"),
    (["help"], "help"),
    (["p", "pay"], "pay"),
    (["pr", "prefix"], "prefix"),
    (["s", "sell"], "sell"),
    (["git"], "git")
]

money = {
    "common": 4,
    "uncommon": 11,
    "rare": 16,
    "legendary": 19,
    "mythic": 22,
    "iconic": 35

}

# it's out of 99 not 100, but whatever
packs = {
    "wood": {
        "cost": 50,
        "count": 7,
        "rarity": {
            "common": 0.0,  # 70%
            "uncommon": 0.7,  # 20%
            "rare": 0.9,  # 5%
            "mythic": 0.95,  # 2%
            "legendary": 0.97,  # 2%
            "iconic": 0.99  # 1%
        }
    },
    "iron": {
        "cost": 125,
        "count": 7,
        "rarity": {
            "common": 0.0,  # 40%
            "uncommon": 0.4,  # 45%
            "rare": 0.85,  # 5%
            "mythic": 0.9,  # 5%
            "legendary": 0.95,  # 3%
            "iconic": 0.98  # 2%
        }
    },
    "gold": {
        "cost": 200,
        "count": 5,
        "rarity": {
            "common": 0.0,  # 30%
            "uncommon": 0.3,  # 40%
            "rare": 0.7,  # 10%
            "mythic": 0.8,  # 10%
            "legendary": 0.9,  # 5%
            "iconic": 0.95  # 5%
        }
    },
    "diamond": {
        "cost": 375,
        "count": 3,
        "rarity": {
            "common": 0.0,  # 10%
            "uncommon": 0.1,  # 30%
            "rare": 0.4,  # 20%
            "mythic": 0.6,  # 20%
            "legendary": 0.8,  # 10%
            "iconic": 0.90  # 10%
        }
    },
}


def create_table():
    c.execute("DROP TABLE IF EXISTS cards;")
    connect.commit()
    c.executescript(f"""
        CREATE TABLE IF NOT EXISTS cards(
            indexer INTEGER PRIMARY KEY, 
            name TEXT UNIQUE, 
            typeo TEXT, 
            class TEXT
        );
        
        CREATE TABLE IF NOT EXISTS users(
            primary_key INTEGER PRIMARY KEY, 
            balance INTEGER, 
            card_ids BLOB
        );
        
        CREATE TABLE IF NOT EXISTS auctions(
            primary_key INTEGER PRIMARY KEY, 
            owner TEXT, 
            bid INTEGER, 
            card_id INTEGER, 
            owner_id INTEGER
        );
        CREATE TABLE IF NOT EXISTS server_configurations(
            primary_key INTEGER PRIMARY KEY, 
            prefix TEXT DEFAULT '{default_prefix}'
        );
    """)
    import_cards()

    #c.execute("DELETE FROM users WHERE primary_key = 223212153207783435;")
    c.execute("SELECT COUNT(*) FROM users")
    result = c.fetchall()

    print(result)
    print(count_all_auctions())
    print(all_auctions(1))
    connect.commit()


def get_prefix(server_id: int):
    c.execute("SELECT prefix FROM server_configurations WHERE primary_key = ?", (server_id, ))
    result = c.fetchone()
    if result is None:
        result = default_prefix
    else:
        result = result[0]
    return result


def set_prefix(server_id: int, value: str):
    c.execute("SELECT prefix FROM server_configurations WHERE primary_key = ?", (server_id, ))
    result = c.fetchone()
    if result is None:
        c.execute("INSERT INTO server_configurations VALUES (?, ?);", (server_id, value,))
    else:
        c.execute("UPDATE server_configurations SET prefix = ? WHERE primary_key = ?", (value, server_id))
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


def get_balance_id(user_id):
    if id is not None:
        c.execute("SELECT balance FROM users WHERE primary_key=?;", (user_id, ))
        result = c.fetchone()
        return result[0]
    else:
        print(f"This user {user_id} has not initialized")
    return False


def add_balance_id(user_id, balance):
    if id is not None:
        c.execute("UPDATE users SET balance= ? WHERE primary_key=?;", (get_balance_id(user_id) + balance, user_id))
        connect.commit()
        return True
    else:
        print(f"This user {user_id} has not initialized")
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
            print(a)
            c.execute("UPDATE users SET card_ids= ? WHERE primary_key=?;", (a, user.id))
            connect.commit()
            return True
        else:
            print(f"This user {user.name} has not initialized")
        return False


def remove_card(user, card_id):
    return sell_card(user, card_id, 1)


def sell_card(user, card_id: int, count: int = 1):
    if get_user(user.id) is not None or get_card_by_id(card_id) is not None:
        cards = get_cards(user)
        a = dict(Counter(cards))
        if count > a[card_id]:
            count = a[card_id] - 1
        if count == 0:
            count += 1
        remove = cards.remove
        for i in range(count):
            remove(card_id)
        c.execute("UPDATE users SET card_ids= ? WHERE primary_key=?;", (json.dumps(cards), user.id))
        connect.commit()
        return count
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
    if not result:
        result = ["?????", "?????", "??????"]
    return result


def get_card_by_ids(card_ids):
    c.execute(f"SELECT * FROM cards WHERE indexer in ({', '.join('?' for _ in card_ids)})", card_ids)
    a = c.fetchall()
    dictionary = dict(Counter(card_ids))
    b = [k for k in a if dictionary[k[1]] for i in range(dictionary[k[1]] - 1)]
    a.extend(b)
    return a


def order_card_ids(card_ids):
    a = get_card_by_ids(card_ids)
    df = pd.DataFrame(a, columns=["row", "indexer", "name", "typeo", "class"]).sort_values(["typeo"])
    return df["indexer"].tolist()


def all_cards(page: int, limit: int = 10, type_: str = "*"):
    if limit == -1 and type_ == "*":
        limit = count_all_cards()
        c.execute("SELECT * FROM cards")
    elif type_ == "*":
        c.execute("SELECT * FROM cards LIMIT ? OFFSET ?;", (limit, limit * page,))
    else:
        c.execute("SELECT * FROM cards WHERE typeo=? LIMIT ?, ?;", (type_, page, limit,))
    return c.fetchall()


def count_user_cards(user, rarity: str = "all"):
    cards = get_cards(user)
    print(cards)
    print(len(cards))
    return len(cards)


def count_all_cards() -> int:
    c.execute("SELECT COUNT (*) FROM cards")
    return c.fetchone()[0]


def get_card(name: str) -> int:
    c.execute("SELECT indexer FROM CARDS WHERE LOWER(name) = LOWER(?) LIMIT 1;", (name, ))
    return c.fetchone()[0]


def get_cards(user):
    if get_user(user.id) is not None:
        c.execute("SELECT card_ids "
                  "FROM users "
                  "WHERE primary_key=?;", (user.id, ))
        cards = c.fetchone()
        cards = ast.literal_eval(cards[0])
        if not cards:
            cards = []
        # else:
        #   cardss = [get_card_by_id(int(c)) for c in cards]
        cards = [int(k) for k in cards]
        a = order_card_ids(cards)
        return a
    else:
        print(f"This user {user.name} has not initialized")
        return False


def buy_pack(user, pack: str, count: int):
    if get_user(user.id) is None:
        print(f"This user {user.name} has not initialized")
        return False
    elif get_balance(user) - packs[pack]["cost"] < 0:
        print(f"This user is in debt")
    else:
        add_balance(user, -packs[pack]["cost"])
        temp = valid_types
        a = []
        append = a.append
        for i in range(count):
            guesser = random.random()
            last = ""
            for valid_type in temp:
                probability = packs[pack]["rarity"][valid_type]
                if guesser >= probability:
                    last = valid_type
                else:
                    break
            possible = all_cards(1, -1, last.capitalize())
            prize = possible[random.randint(0, len(possible)-1)]
            append(prize)
            print(f"{pack} {guesser} - {last} - {prize}")
        d = np.array(a)
        add_card(user, d[:, 1].tolist())
        return a


def get_auction(auction_id: int or list) -> list:
    if isinstance(auction_id, int):
        query = f"SELECT * FROM auctions WHERE primary_key = ?"
        c.execute(query, (auction_id,))
    else:
        query = f"SELECT * FROM auctions WHERE primary_key in ({', '.join('?' for _ in auction_id)})"
        c.execute(query, auction_id)
    return c.fetchall()


def all_auctions(page: int, limit: int = 10):
    if limit == -1:
        c.execute("SELECT * FROM auctions")
    else:
        c.execute("SELECT * FROM auctions LIMIT ? OFFSET ?;", (limit, limit * page,))
    return c.fetchall()


def count_all_auctions() -> int:
    c.execute("SELECT COUNT (*) FROM auctions")
    return c.fetchone()[0]


def add_auction(user, card_id: int, bid_amount: int):
    c.execute("INSERT INTO auctions VALUES (?, ?, ?, ?, ?);", (count_all_auctions(), user.name, bid_amount, card_id, user.id))
    connect.commit()


def remove_auction(auction_id: int):
    c.execute("DELETE FROM auctions WHERE primary_key = ?;", (auction_id,))
    connect.commit()


def check_auction(auction_id: int) -> bool:
    c.execute("SELECT * FROM auctions WHERE primary_key = ?", (auction_id, ))
    return len(c.fetchone()) > 0
