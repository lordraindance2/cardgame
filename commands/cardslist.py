from .runner import Runner
import discord
import database
import numpy as np
import util
import discord


class CardsListCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "cardslist_command"

    def do(self):
        super().do()
        if int(self.sender.id) != 223212153207783435:
            pass
        embed = discord.Embed(descrption="List of Cards", color=discord.Color.dark_blue())
        # change the values so they work in discord.py
        embed.set_author(name=self.sender.name, icon_url=self.client.user.avatar_url)
        if len(self.args) == 1:
            try:
                page = int(self.args[0]) - 1
            except ValueError:
                return f"{self.args[0]} is not a page number", None
        elif len(self.args) == 0:
            page = 0
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
        result = database.all_cards(page=page)
        cleaned_results = [f"{util.escape_underscore(r[1])} :: {r[2]} :: {r[3]}" for r in result]
        embed.add_field(name="Cards", value="\n".join(cleaned_results), inline=False)
        max_pages = int(np.ceil(database.count_all_cards() / 10))
        embed.set_footer(text=f"Showing page {page + 1} of {max_pages - 1}")
        return None, embed
