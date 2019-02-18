import discord
import asyncio
import logging
import database
import re
import importlib
import datetime
import random
from config import get_prefix, prefix
from commands import CardslistCommand
import os
from boto.s3.connection import S3Connection

s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

game = discord.Game(name="!help - RainDance🌧#4115 for help/other", url="https://www.twitch.tv/lordraindance")
client = discord.Client()

user_time_dict = {}


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    database.create_table()
    print(str(database.connect))
    print("hello")
    print(database.show_table())
    await client.change_presence(game=game)


@client.event
async def on_message(message):
    msg = message.content.strip()
    if database.get_user(message.author.id) is not None:
        if message.author.id in user_time_dict.keys():
            if datetime.datetime.utcnow() - user_time_dict[message.author.id] > datetime.timedelta(minutes=1):
                database.add_balance(message.author, int(random.uniform(9, 15)))
                user_time_dict[message.author.id] = datetime.datetime.utcnow()
        else:
            user_time_dict[message.author.id] = datetime.datetime.utcnow()
    if msg.startswith(get_prefix(hash(message.server))):
        _command = msg.split(" ")[0]
        args = re.sub(" +", " ", msg).split(" ")[1:]
        # clean_command = re.sub(get_prefix(hash(message.server)), "", _command)
        clean_command = _command[(len(get_prefix(hash(message.server)))):]
        try:
            print(f"{clean_command.capitalize()}Command")
            mod = __import__("commands", fromlist=[f"{clean_command.capitalize()}Command"])
            comm = getattr(mod, f"{clean_command.capitalize()}Command")
            b = comm(client, message, message.author, args)
            a = b.do()
            if isinstance(a, tuple):
                text, embed = a
            else:
                text = a
                embed = None
            #if text is None:
            #    text = ""
            a = await client.send_message(destination=message.channel, content=text, embed=embed)
        except Exception:
            print(f"Exception!")
            logging.exception(Exception)

    """
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!hello'):
        await client.send_message(message.channel, f"{message.channel.name}")
    """

client.run(os.environ['bot_token'])
