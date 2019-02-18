from .runner import Runner
import database
import json
import util
import numpy as np
import discord


class CardsCommand(Runner):

    def __init__(self, client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "cards_command"

    def do(self):
        super().do()
        if len(self.args) == 1:
            try:
                page = int(self.args[0]) - 1
            except ValueError:
                return f"{page} isn't a number!"
        elif len(self.args) == 0:
            page = 0
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
        data = database.get_user(self.sender.id)
        id = data[0]
        balance = data[1]
        cards = database.get_cards(self.sender)
        if not cards:
            return "0 cards"
        if data is not None:
            a = [database.get_card_by_id(c) for c in cards]
            b = np.array(a)
            pages = int(len(b) / 10)
            offset = page * 11
            b = b[offset:offset + 10]
            a = [f"{util.escape_underscore(s[0])} :: {s[1]} :: {s[2]}" for s in b[:, 2:]]
            output = "\n".join(a)

            embed = discord.Embed(descrption=f"{self.sender.name}: List of Cards", color=discord.Color.red())
            # change the values so they work in discord.py
            embed.set_author(name=self.sender.name, icon_url=self.sender.avatar_url)
            embed.add_field(name="Current Balance:", value=balance, inline=False)
            embed.add_field(name="Cards", value=output, inline=False)
            embed.set_footer(text=f"Showing page {page + 1} of {pages + 1}")
            return None, embed
        else:
            return f"You did not initialize yourself! Do !start to do so."

