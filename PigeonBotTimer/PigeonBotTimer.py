#bot.py
import os
import sys
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import csv
import praw
import json

commandsList = []

bot = commands.Bot(command_prefix="=")

token = "REDACTED"

tagList = {
    'https://i.redd.it/qe3igt2qau251.jpg': 'Iz Myrtle',
    'https://i.redd.it/hllvel56zw451.jpg': 'Iz Pete'

}

images = open("..\last20.txt")
imageslist = images.read().splitlines()
images.close()
badpigeons = open("..\\badpigeons.txt")
badpigeonslist = badpigeons.read().splitlines()
badpigeons.close()
def getKey(key): 
    if key in tagList.keys(): 
        return(tagList[key] + ' ');
    else:
        return('');

@bot.event
async def on_ready():
    channel = bot.get_channel(674755201575419936)

    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='Pigeon Grabber by HurricaneSYG')

    while True:
        submission = reddit.subreddit("pigeon").random()
        if (submission.url in badpigeonslist):
            print("badbot")
        elif (submission.url in imageslist):
            print("No")
        elif (submission.url.endswith(".jpg")) or (submission.url.endswith(".png") or (submission.url.endswith(".gif"))):
            channel = bot.get_channel(674755201575419936)
            tagLine = getKey(submission.url)

            imageslist.pop(0)
            imageslist.append(submission.url)

            f = open("..\last20.txt", "w")
            f.write('\n'.join(imageslist))
            f.close()
            await channel.send(tagLine + submission.url)
            break
    sys.exit("Done")


bot.run(token)
