from .runner import Runner
import database
import json
from numbers import Number
import discord
import util


class AuctionCommand(Runner):

    def __init__(self, client, server, message, sender, args):
        super().__init__(client, ..., message, sender, args)
        self.name = "add_command"

    def do(self):
        super().do()
        embed = discord.Embed(descrption="Auctions", color=discord.Color.red())
        embed.set_author(name=self.sender.name, icon_url=self.client.user.avatar_url)

        page = 0
        if len(self.args) == 1:
            try:
                page = int(self.args[0])
            except ValueError:
                return f"{self.args[0]} is not a valid number"
        if len(self.args) == 0:
            # change the values so they work in discord.py
            auctions = database.all_auctions(page)
            print(auctions)
            if len(auctions) == 0:
                return "No auctions"
            cleaned_results = [f"{r[0]} :: {util.escape_underscore(r[1])} :: " 
                               f"{r[2]} :: {database.get_card_by_id(r[3])[2]}"
                               for r in auctions]
            embed.add_field(name="Auctions(id::owner::money::card)", value="\n".join(cleaned_results), inline=False)
            embed.set_footer(
                text=f"Showing page {page + 1} of {int(database.count_all_auctions() / 10) + 1}")
            return None, embed
        if self.args[0] == "accept" and self.args[1]:
            try:
                auction_id = int(self.args[1])
                if not database.check_auction(auction_id):
                    return f"{self.args[1]} is not a valid auction id!"
            except ValueError:
                return f"{self.args[1]} is not a valid auction id!"
            # here:
            auction = database.get_auction(auction_id)[0]
            print(auction)
            if database.get_balance(self.sender) >= auction[2]:
                database.remove_auction(auction[0])
                database.add_card(self.sender, auction[3])
                database.add_balance(self.sender, -auction[2])
                database.add_balance_id(auction[4], auction[2])
                return f"You earned {database.get_card_by_id(auction[3])[2]} " \
                       f"from an auction with a bid of {auction[2]}"
            else:
                return "You do not have enough money to accept that auction!"
        elif self.args[0] == "revoke" and self.args[1]:
            try:
                auction_id = int(self.args[1])
                if not database.check_auction(auction_id):
                    return f"{self.args[1]} is not a valid auction id!"
            except ValueError:
                return f"{self.args[1]} is not a valid auction id!"
            auction = database.get_auction(auction_id)[0]
            database.remove_auction(auction[0])
            database.add_card(self.sender, auction[3])
            return f"You revoked auction {auction_id}"
        elif len(self.args) == 2:
            try:
                bid_balance = int(self.args[1])
                card_id = database.get_card(self.args[0])
            except ValueError:
                return f"{self.args[1]} is not a valid number"
            if card_id is not None:
                if card_id in database.get_cards(self.sender):
                    full_card = database.get_card_by_id(card_id)
                    database.add_auction(self.sender, card_id, bid_balance)
                    c = database.remove_card(self.sender, card_id)
                    print(c)
                    if c:
                        return f"You put {full_card[2]} up for auction for {bid_balance} money"
                    else:
                        print("Error in auctioning card")
                else:
                    return f"You do not have that card!"
            else:
                return f"Invalid card"

