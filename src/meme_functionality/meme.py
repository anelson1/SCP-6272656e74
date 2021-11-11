"""Helper class for all meme generation functions"""
import random
import os
import json
import shutil
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import requests
import discord

def resize(image):
    """resize image"""
    img = Image.open(image)
    img.save("src/meme_functionality/images/temp.jpg",optimize = True, quality = 10)

async def fetch_meme(message):
    """Fetch memes from a cursed image sub-reddit to use with our meme making function"""
    url_list= ['https://www.reddit.com/r/FunnyCursedImages.json',
               'https://www.reddit.com/r/blursedimages.json',
               'https://www.reddit.com/r/MemeTemplatesOfficial.json',
               'https://www.reddit.com/r/MemeTemplatesIta.json']
    response_api = requests.get(random.choice(url_list), headers={'User-agent': 'Based Bot 1.0'})
    if not response_api.ok:
        print("Error", response_api.status_code)
        await message.channel.send("Slow down on the memes buddy")
        return "error"
    data = response_api.text
    parsed_data= json.loads(data)
    image_url = parsed_data["data"]["children"][
        random.randint(2,len(parsed_data["data"]["children"])-1)
        ]["data"]["url_overridden_by_dest"]
    resp = requests.get(image_url, stream=True)
    local_file = open('src/meme_functionality/images/temp.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    if is_image_greater_then_8_mb():
        print("Image too big, getting another")
        await fetch_meme(message)


def is_image_greater_then_8_mb():
    """Check and see if gotten image is >8MB"""
    file_path = 'src/meme_functionality/images/temp.jpg'
    file_size = os.path.getsize(file_path)
    if file_size/1024**2 > 8:
        return True
    return False


async def roulette(ctx, caption):
    """Random chance that any message sent will turn into a meme"""
    check = random.randint(1, 100)
    if check == 1:
        await shitpost(ctx, caption)


def find_space(text):
    """Split parameter into top and bottom text"""
    midpoint = int(len(text)/2)
    if text[midpoint] != ' ':
        for i in text[int(len(text)/2)::]:
            if i == ' ':
                return midpoint
            midpoint += 1
    return midpoint

async def shitpost(ctx, caption):
    """Handler to load in text and image to meme maker"""
    print("Initaiting Shitposting Sequence")
    async with ctx.message.channel.typing():
        flag = await fetch_meme(caption)
        print("Meme has been fetched")
        if flag == "error":
            return
        text = caption
        midpoint = find_space(text)
        text1 = text[0:midpoint]
        text2 = text[midpoint+1::]
        image = "src/meme_functionality/images/temp.jpg"
        sent = await ctx.send("Making meme...")
        try:
            make_meme(text1, text2, image)
        except:
            print("Error making meme, trying again")
            await sent.delete()
            await shitpost(ctx, caption)
            return
        print("Meme has been made")
        await ctx.send(file=discord.File('src/meme_functionality/images/output/output.jpg'))
        await sent.delete()

def make_meme(top_string, bottom_string, filename):
    """Logic to generate meme"""
    resize(filename)
    print("Meme is being made")
    img = Image.open(filename)
    image_size = img.size
    # find biggest font size that works
    font_size = int(image_size[1]/5)
    font = ImageFont.truetype("src/meme_functionality/impact.ttf", font_size)
    top_text_size = font.getsize(top_string)
    bottom_text_size = font.getsize(bottom_string)
    while top_text_size[0] > image_size[0]-20 or bottom_text_size[0] > image_size[0]-20:
        font_size = font_size - 1
        font = ImageFont.truetype("src/meme_functionality/impact.ttf", font_size)
        top_text_size = font.getsize(top_string)
        bottom_text_size = font.getsize(bottom_string)
    # find top centered position for top text
    top_text_pos_x = (image_size[0]/2) - (top_text_size[0]/2)
    top_text_pos_y = 0
    top_text_pos = (top_text_pos_x, top_text_pos_y)
    # find bottom centered position for bottom text
    bottom_text_pos_x = (image_size[0]/2) - (bottom_text_size[0]/2)
    bottom_text_pos_y = image_size[1] - bottom_text_size[1]
    bottom_text_pos = (bottom_text_pos_x, bottom_text_pos_y)
    draw = ImageDraw.Draw(img)
    # draw outlines
    # there may be a better way
    outline_range = int(font_size/15)
    for x_pos in range(-outline_range, outline_range+1):
        for y_pos in range(-outline_range, outline_range+1):
            draw.text(
                (top_text_pos[0]+x_pos,
                 top_text_pos[1]+y_pos),
                top_string,
                (0, 0, 0),
                font=font)
            draw.text(
                (bottom_text_pos[0]+x_pos,
                 bottom_text_pos[1]+y_pos),
                bottom_string,
                (0, 0, 0),
                font=font)
    draw.text(top_text_pos, top_string, (255, 255, 255), font=font)
    draw.text(bottom_text_pos, bottom_string, (255, 255, 255), font=font)
    img.save("src/meme_functionality/images/output/output.jpg", optimize = True, quality = 30)
