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

bot = commands.Bot(command_prefix="=", self_bot=True)

token = "REDACTED"

tagList = {
    'https://i.redd.it/qe3igt2qau251.jpg': 'Iz Myrtle',
    'https://i.redd.it/hllvel56zw451.jpg': 'Iz Pete'

}

def getKey(key): 
    if key in tagList.keys(): 
        return(tagList[key] + ' ');
    else:
        return('');

@bot.event
async def on_ready():
    badBirds = ["https://i.redd.it/j7v2m32k5od51.jpg"]
    channel = bot.get_channel(674755201575419936)

    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='Pigeon Grabber by HurricaneSYG')

    while True:
        submission = reddit.subreddit("pigeon").random()
        if (submission.url in badBirds):
            print("badbot")
        elif (submission.url.endswith(".jpg")) or (submission.url.endswith(".png") or (submission.url.endswith(".gif"))):
            channel = bot.get_channel(674755201575419936)
            tagLine = getKey(submission.url);
            await channel.send(tagLine + submission.url)
            break
    quit()


bot.run(token)
