from .runner import Runner
import database
import random
import discord


class GambleCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "gamble_command"

    def do(self):
        super().do()
        if len(self.args) == 0:
            cards = database.all_cards(1, -1)
            a = random.random()
            possible = int(a * (len(cards) - 1))
            if database.get_balance(self.sender) - 1000 < 0:
                return "You do not have enough money to partake in your gamble"
            print(f"{a} {possible}")
            if database.add_balance(self.sender, - 1000) and database.add_card(self.sender, possible):
                embed = discord.Embed(descrption=f"{self.sender.name}: Gamble",
                                      color=discord.Color.dark_gold())
                # change the values so they work in discord.py
                embed.set_author(name="Gamble Discovery", icon_url=self.sender.avatar_url)
                card = database.get_card_by_id(possible)
                embed.add_field(name="Result", value=f":star: You gambled for {card[2]} :star:", inline=False)

                embed.set_footer(text=f"{self.sender.name}'s Gamble")
                return None, embed
            return f""
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
