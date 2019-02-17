from .runner import Runner
import database
import json
from numbers import Number
import discord
import numpy as np
import util


class BuyCommand(Runner):

    def __init__(self,client,  message, sender, args):
        super().__init__(client, message, sender, args)
        self.name = "buy_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            return f"""Available packs: {', '.join([f"{k.capitalize()}: {database.packs[k]['cost']}" for k in database.packs.keys()])}"""
        if len(self.args) == 1:
            if database.get_user(self.sender.id) is None:
                return "forgot to do !start"
            elif self.args[0] not in database.packs.keys():
                return f"Valid packs include: {str([k for k in database.packs.keys()])}"
            elif database.get_balance(self.sender) - database.packs[self.args[0]]["cost"] < 0:
                return "please do not put yourself in debt"
            else:
                pack = database.buy_pack(self.sender, self.args[0])
                if pack:
                    embed = discord.Embed(title=f"{(self.args[0]).capitalize()}: Discovery", color=discord.Color.green())
                    # change the values so they work in discord.py
                    embed.set_author(name=self.sender.name, icon_url=self.sender.avatar_url)

                    b = np.array(pack)
                    a = [f"{util.escape_underscore(s[0])} :: {s[1]} :: {s[2]}" for s in b[:, 2:]]
                    embed.add_field(name="Cards", value="\n".join(a), inline=False)
                    return None, embed
        else:
            return f"command {self.name} has too many or too few arguments ( {self.args})"
