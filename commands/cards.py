from .runner import Runner
import database
import util
import numpy as np
import discord


class CardsCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, server, message, sender, args)
        self.name = "cards_command"

    def do(self):
        super().do()
        if len(self.args) == 1:
            try:
                page = int(self.args[0])
                if page <= 0:
                    page = 1
            except ValueError:
                return f"{page} isn't a number!"
        elif len(self.args) == 0:
            page = 1
        else:
            return f"command {self.name} has too many arguments ( {self.args})"
        data = database.get_user(self.sender.id)
        id = data[0]
        balance = data[1]
        cards = database.get_cards(self.sender)
        print("####")
        print(cards)
        if not cards:
            return "0 cards"
        if data is not None:
            unique, counts = np.unique(np.array(cards), return_counts=True)
            dictionary = dict(zip(unique, counts))
            count_of_all_cards = list(dictionary.values())

            b = database.get_card_by_ids(unique.tolist())
            sorted_cards = []
            for i, bb in enumerate(b):
                original = list(bb).copy()
                it_count = count_of_all_cards[i]
                original.append(it_count)
                sorted_cards.append(original)
            sorted_cards = np.array(sorted_cards)

            max_pages = int(np.ceil(len(sorted_cards) / 10))
            print(max_pages)
            page -= 1
            offset = page * 10
            b = sorted_cards[offset:offset + 9]
            a = [f"{util.escape_underscore(s[0])} :: {s[1]} :: {s[2]} x{s[3]}" for s in b[:, 2:]]
            output = "\n".join(a)

            embed = discord.Embed(descrption=f"{self.sender.name}: List of Cards", color=discord.Color.red())
            # change the values so they work in discord.py
            embed.set_author(name=self.sender.name, icon_url=self.sender.avatar_url)
            soon_to_be_list_of_cards = database.count_user_cards(self.sender, "all")
            embed.add_field(name=f"Card Count: {soon_to_be_list_of_cards}", value=output, inline=False)

            embed.set_footer(text=f"{self.sender.name}: Showing page {page + 1} of {max_pages}")
            return None, embed
        else:
            return f"You did not initialize yourself! Do !start to do so."

