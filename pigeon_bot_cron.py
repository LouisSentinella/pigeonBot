import os
import sys

from dotenv import load_dotenv
import random

import discord
from discord.ext import commands
import praw

commandsList = []

load_dotenv()

CLIENT_ID=os.getenv('CLIENT_ID')
CLIENT_SECRET=os.getenv('CLIENT_SECRET')
DISCORD_TOKEN=os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix="=", intents=discord.Intents(messages=True, message_content=True, guilds=True))

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='Pigeon Grabber by HurricaneSYG',
                     check_for_async=False)

tagList = {
    'https://i.redd.it/qe3igt2qau251.jpg': 'Iz Myrtle',
    'https://i.redd.it/hllvel56zw451.jpg': 'Iz Pete'

}

recent_images = open("last20.txt")
images_list = recent_images.read().splitlines()
recent_images.close()
bad_pigeons = open("badpigeons.txt")
bad_pigeons_list = bad_pigeons.read().splitlines()
bad_pigeons.close()

def getKey(key):
    if key in tagList.keys():
        return(tagList[key] + ' ')
    else:
        return('')

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
    channel = bot.get_channel(674755201575419936)

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
    await channel.send(tagLine + selected_url)

    sys.exit()

bot.run(DISCORD_TOKEN)
