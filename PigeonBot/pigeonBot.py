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
import json
from datetime import datetime

commandsList = []

bot = commands.Bot(command_prefix="=")

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

imageSent = None

badPeople2 = ["camelus#4766"]
badPeople = [698505803090493520]
start = time.time()

@bot.event
async def on_ready():
    print ("Ready")


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



@bot.command(name='gimmeapigeon')
async def gimmeapigeon(ctx):
    global start
    timeNow = time.time()
    reddit = praw.Reddit(client_id='REDACTED',
                         client_secret='REDACTED',
                         user_agent='Pigeon Grabber by HurricaneSYG')
    if (timeNow - start > 20):
        while True:
            submission = reddit.subreddit("pigeon").random()
            if (submission.url == "https://i.redd.it/j7v2m32k5od51.jpg"):
                print("badbot")
            elif (submission.url.endswith(".jpg")) or submission.url.endswith(".png") or (submission.url.endswith(".gif")):
                tagLine = getKey(submission.url);
                await ctx.send(tagLine + submission.url)
                start = time.time() 
                break

@bot.event
async def on_message(message):
    if (message.author == bot.user):
	    return
    #print(message.author.id)
    if (message.author.id in badPeople):
        return
   
    await bot.process_commands(message)


bot.run(token)






