from .runner import Runner
import database
import json
from numbers import Number
import discord


class HelpCommand(Runner):

    def __init__(self, client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "balance_command"

    def do(self):
        super().do()
        embed = discord.Embed(title=f"List of Commands", color=discord.Color.dark_blue())
        # change the values so they work in discord.py
        embed.set_author(name="by RainDance", icon_url="https://poketouch.files.wordpress.com/2016/08/freeze_pokemon_articuno.png?w=648")

        a = ["!start - Do this to start your card game adventure!",
             "!balance - Check your money!",
             "!buy - Buy a pack, run '!buy' for more details!",
             "!cards - Find out your list of cards!",
             "!cardslist - Find out the total list of cards!",
             "!help - This command!",
             "!pay - Pay someone of your choice an amount of money!",
             "!prefix - Change the server prefix or view the current",
             "!sell - Sell a card for money"]

        embed.add_field(name="Commands", value="\n".join(a), inline=False)
        return None, embed
