# bot.py


import discord
from discord.ext import commands

import praw
import time
import math

bot = commands.Bot(command_prefix="=")

tagList = {
    'https://i.redd.it/qe3igt2qau251.jpg': 'Iz Myrtle',
    'https://i.redd.it/hllvel56zw451.jpg': 'Iz Pete'

}


def getKey(key):
    if key in tagList.keys():
        return tagList[key] + ' '
    else:
        return ''


badPeople2 = ["camelus#4766"]
badPeople = [698505803090493520]
start = time.time()

images = open("..\last20.txt")
imageslist = images.read().splitlines()
images.close()

badpigeons = open("..\\badpigeons.txt")
badpigeonslist = badpigeons.read().splitlines()
badpigeons.close()

badpigeonadded = False

@bot.event
async def on_ready():
    print("Ready")


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
    await ctx.send(timeList[math.ceil(nothingInt)] + " GMT")


@bot.command(name='plsbotnotthatimage')
async def plsbotnotthatimage(ctx):
    global badpigeonadded
    f = open("..\\badpigeons.txt", "w")
    badpigeonslist.append(imageslist[-1])
    f.write('\n'.join(badpigeonslist))
    f.close()
    badpigeonadded = True
    await ctx.send("dw guys, that image will not be sent anymore!")


@bot.command(name='iwaswrongbb')
async def iwaswrongbb(ctx):
    global badpigeonadded
    if badpigeonadded:
        f = open("..\\badpigeons.txt", "w")
        badpigeonslist.pop(-1)
        f.write('\n'.join(badpigeonslist))
        f.close()
        badpigeonadded = False
        await ctx.send("you silly goose, dw <3 i've removed it from the list of bad pigeons")
    else:
        await ctx.send("I'm not gonna lie, no bad pigeon has been added to the list since last time...")

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
            if (submission.url in badpigeonslist):
                print("badbot")
            elif (submission.url in imageslist):
                print("No")
            elif (submission.url.endswith(".jpg")) or (
                    submission.url.endswith(".png") or (submission.url.endswith(".gif"))):
                channel = bot.get_channel(674755201575419936)
                tagLine = getKey(submission.url)

                imageslist.pop(0)
                imageslist.append(submission.url)

                f = open("..\last20.txt", "w")
                f.write('\n'.join(imageslist))
                f.close()
                await channel.send(tagLine + submission.url)
                break


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id in badPeople:
        return

    await bot.process_commands(message)


bot.run('REDACTED')
