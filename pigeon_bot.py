# bot.py
import random

import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

import praw
import time
import math

load_dotenv()

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')

badPeople2 = ["camelus#4766"]
badPeople = [698505803090493520]
start = time.time()

bad_pigeon_added = False

bot = commands.Bot(command_prefix="=", intents=discord.Intents(messages=True, message_content=True, guilds=True))

tagList = {
    'https://i.redd.it/qe3igt2qau251.jpg': 'Iz Myrtle',
    'https://i.redd.it/hllvel56zw451.jpg': 'Iz Pete'

}

def getKey(key):
    if key in tagList.keys():
        return tagList[key] + ' '
    else:
        return ''

def handle_submission(submission):

    if submission.over_18:
        return []

    if True in [submission.url.endswith(i) for i in ['.jpg', '.jpeg', '.png', '.gif']]:
        return [submission.url]
    elif 'gallery' in submission.url:
        if hasattr(submission, 'media_metadata'):
            image_dict = submission.media_metadata
            urls = []
            for image_item in image_dict.values():
                largest_image = image_item['s']
                image_url = largest_image['u']
                question_mark_index = image_url.index('?')
                urls.append(image_url[:question_mark_index].replace('preview', 'i'))
            return urls
        else:
            return []
    elif 'v.redd.it' in submission.url:
        media_url = submission.media['reddit_video']['fallback_url']
        trimmed_media_url = media_url[:media_url.index('?')]
        return [trimmed_media_url]
    else:
        return []

@bot.event
async def on_ready():
    print("Ready")


@bot.command(name='whenisnextpigeon', brief="Tells you when the next scheduled pigeon is")
async def whenisnextpigeon(ctx):
    timeList = ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "00:00"]
    timeTest = time.asctime(time.localtime(time.time()))
    newTime = timeTest.split()

    justTime = newTime[3]
    nothingElse = justTime[0:2]
    nothingInt = int(nothingElse)

    nothingInt += 0.1
    nothingInt = nothingInt / 4
    await ctx.send(timeList[math.ceil(nothingInt)] + " UTC")


@bot.command(name='plsbotnotthatimage', brief="Adds the last image to a list of images never to post")
async def plsbotnotthatimage(ctx):
    global bad_pigeon_added
    bad_pigeons = open("badpigeons.txt")
    bad_pigeons_list = bad_pigeons.read().splitlines()
    bad_pigeons.close()
    recent_images = open("last20.txt")
    images_list = recent_images.read().splitlines()
    recent_images.close()
    f = open("badpigeons.txt", "w")
    bad_pigeons_list.append(images_list[-1])
    f.write('\n'.join(bad_pigeons_list))
    f.close()
    bad_pigeon_added = True
    await ctx.send("That image will not be sent anymore!")


@bot.command(name='iwaswrongbb', brief="Removes the last image from the list not to post")
async def iwaswrongbb(ctx):
    global bad_pigeon_added
    if bad_pigeon_added:
        bad_pigeons = open("badpigeons.txt")
        bad_pigeons_list = bad_pigeons.read().splitlines()
        bad_pigeons.close()
        f = open("badpigeons.txt", "w")
        bad_pigeons_list.pop(-1)
        f.write('\n'.join(bad_pigeons_list))
        f.close()
        bad_pigeon_added = False
        await ctx.send("You silly goose, dw <3 i've removed it from the list of bad pigeons")
    else:
        await ctx.send("No bad pigeon has been added to the list since last time...")

@bot.command(name='gimmeapigeon', brief="Posts random pigeon pic")
async def gimmeapigeon(ctx):

    print("Getting pigeon")
    global start
    recent_images = open("last20.txt")
    images_list = recent_images.read().splitlines()
    recent_images.close()
    bad_pigeons = open("badpigeons.txt")
    bad_pigeons_list = bad_pigeons.read().splitlines()
    bad_pigeons.close()
    timeNow = time.time()
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent='Pigeon Grabber by HurricaneSYG',
                         check_for_async=False)
    if (timeNow - start > 20):
        urls = []
        for i in range(10):
            submission = reddit.subreddit("pigeon").random()
            urls.extend(handle_submission(submission))

        print(urls)
        image_selected = False
        while not image_selected:
            selected_url = random.choice(urls)
            if selected_url in bad_pigeons_list:
                print('badbot')
            elif selected_url in images_list:
                print("The image", selected_url, "was not printed because ", selected_url in images_list)
            else:
                image_selected = True

        tagLine = getKey(selected_url)
        images_list.pop(0)
        images_list.append(selected_url)
        f = open("last20.txt", "w")
        f.write('\n'.join(images_list))
        f.close()
        await ctx.send(tagLine + selected_url)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.id in badPeople:
        return

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
