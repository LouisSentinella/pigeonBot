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
    await ctx.send(nextPigeonTime + " GMT")



@bot.event
async def on_message(message):
    if (message.author == bot.user) and (message.content != "*imageSent"):
        return
    if message.content == "*imageSent":
        timeTest = time.asctime(time.localtime(time.time()))
        newTime = timeTest.split()

        justTime = newTime[3]
        justHour = justTime[0:2]
        everythingElse = justTime[2:8]
        justNextHourInt = int(justHour) + 4

        if justNextHourInt > 24:
            justNextHourStr = "0" + str(justNextHourInt - 24)
        elif (justNextHourInt == 24):
            justNextHourStr = "00"
        else:
            justNextHourStr = str(justNextHourInt)

        newTimeNext = justNextHourStr + everythingElse
        global nextPigeonTime
        nextPigeonTime = newTimeNext[0:5]
    await bot.process_commands(message)


bot.run(token)






