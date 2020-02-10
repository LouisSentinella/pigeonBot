#bot.py
import os
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import csv
import praw
import time

commandsList = []

bot = commands.Bot(command_prefix="=", self_bot=True)

token = "REDACTED"




@bot.event
async def on_ready():
    channel = bot.get_channel(674755201575419936)
    await channel.send(file=discord.File('restart.jpg'))
    await startTimer()

@bot.command(name='gimmeapigeon')
async def gimmeapigeon(ctx):
    return

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


async def startTimer():
    timeList = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"]
    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='REDACTED')
    while True:
        timeTest = time.asctime(time.localtime(time.time()))
        newTime = timeTest.split()

        justTime = newTime[3]
        nothingElse = justTime[0:5]
        if nothingElse in timeList:
            while True:
                submission = reddit.subreddit("pigeon").random()

                if (submission.url.endswith(".jpg")) or (submission.url.endswith(".gif")):
                    channel = bot.get_channel(674755201575419936)
                    await channel.send(submission.url)
                    break
            break
        else:
            print("sleeping")
            time.sleep(60)

    while True:
        for i in range(0, 12):
            print("wake up")
            time.sleep(1200)

        while True:
            submission = reddit.subreddit("pigeon").random()

            if (submission.url.endswith(".jpg")) or (submission.url.endswith(".gif")):
                channel = bot.get_channel(674755201575419936)
                await channel.send(submission.url)
                break


bot.run(token)






