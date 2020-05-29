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
import math


commandsList = []

bot = commands.Bot(command_prefix="=")

token = "REDACTED"

imageSent = None



@bot.event
async def on_ready():
    print ("Ready")


@bot.command(name='gimmeapigeon')
async def gimmeapigeon(ctx):

    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='REDACTED')

    while True:


        submission = reddit.subreddit("pigeon").random()

        if (submission.url.endswith(".jpg")) or (submission.url.endswith(".gif")):
            await ctx.send(submission.url)
        break



@bot.command(name='whenisnextpigeon')
async def whenisnextpigeon(ctx):
    timeList = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "00:00"]
    timeTest = time.asctime(time.localtime(time.time()))
    newTime = timeTest.split()

    justTime = newTime[3]
    nothingElse = justTime[0:2]
    nothingInt = int(nothingElse)

    nothingInt += 0.1
    nothingInt = nothingInt / 4
    await ctx.send( timeList[math.ceil(nothingInt)] + " GMT")



@bot.event
async def on_message(message):
    if (message.author == bot.user):
        return

    await bot.process_commands(message)


bot.run(token)






