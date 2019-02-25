import discord
import asyncio
import logging
import database
import re
import importlib
import datetime
import random
from commands import CardslistCommand
import os
from boto.s3.connection import S3Connection

#s3 = S3Connection("STUPIDHASH", "TOTALLYSECURE")
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

game = discord.Game(name="$help - RainDance🌧#4115 for help/other", url="https://www.twitch.tv/lordraindance")
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
    a = await client.get_user_info('223212153207783435')
    print(a)
    await client.change_presence(game=game)


@client.event
async def on_message(message):
    msg = message.content.strip()
    if not message.author.bot:
        if database.get_user(message.author.id) is not None:
            if message.author.id in user_time_dict.keys():
                if datetime.datetime.utcnow() - user_time_dict[message.author.id] > datetime.timedelta(minutes=1):
                    database.add_balance(message.author, int(random.uniform(9, 15)))
                    user_time_dict[message.author.id] = datetime.datetime.utcnow()
            else:
                user_time_dict[message.author.id] = datetime.datetime.utcnow()
        else:
            database.init_user(message.author)
            database.add_balance(message.author, 50)
    server_id = int(message.server.id)
    if message.server.id == 542778736857317386 and message.id not in [542783664023535616]:
        pass
    if msg.startswith(database.get_prefix(server_id)):
        _command = msg.split(" ")[0].lower()
        args = re.sub(" +", " ", msg).split(" ")[1:]
        # clean_command = re.sub(get_prefix(hash(message.server)), "", _command)
        prefix = database.get_prefix(server_id)
        clean_command = _command[(len(prefix)):]
        for k in database.command_alias:
            if clean_command in k[0]:
                clean_command = k[1]
                break
        try:
            print(f"{message.author.name} runs {clean_command.capitalize()}Command with {args}")
            mod = __import__("commands", fromlist=[f"{clean_command.capitalize()}Command"])
            comm = getattr(mod, f"{clean_command.capitalize()}Command")
            b = comm(client, message.server, message, message.author, args)
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
print(os.environ["CARD_GAME_BOT_TOKEN"])
client.run(os.environ["CARD_GAME_BOT_TOKEN"])
