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




@bot.event
async def on_ready():
    print ("Ready")


@bot.command(name='gimmeapigeon')
async def gimmeapigeon(ctx):
    return

@bot.command(name='startTimer')
async def startTimer(ctx):
    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='REDACTED')

    while True:
        while True:

            submission = reddit.subreddit("pigeon").random()

            if (submission.url.endswith(".jpg")) or (submission.url.endswith(".gif")):
                await ctx.send(submission.url)
                channel = bot.get_channel("REDACTED")
                await channel.send("*imageSent")
                break
        for i in range(0, 12):
            print("wake up")
            time.sleep(1200)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


bot.run(token)






