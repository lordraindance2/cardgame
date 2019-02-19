from .runner import Runner
import discord
import database
import numpy as np
import util
import discord

class CardsListCommand(Runner):

    def __init__(self,client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "cardslist_command"

    def do(self):
        super().do()
        embed = discord.Embed(descrption="List of Cards", color=discord.Color.dark_blue())
        # change the values so they work in discord.py
        embed.set_author(name=self.sender.name, icon_url=self.client.user.avatar_url)
        if len(self.args) == 1:
            try:
                page = int(self.args[0])
            except ValueError:
                return f"{self.args[0]} is not a page number", None
        elif len(self.args) == 0:
            page = 1
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
        result = database.all_cards(page=page)
        print(result)
        cleaned_results = [f"{util.escape_underscore(r[2])} :: {r[3]} :: {r[4]}" for r in result]
        embed.add_field(name="Cards", value="\n".join(cleaned_results), inline=False)
        embed.set_footer(text=f"Showing page {page} of {int(database.count_all_cards() / 10)}")
        return None, embed
