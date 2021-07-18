from src import discord
import random
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

# Random chance that any message sent will turn into a meme


async def roulette(message):
    check = random.randint(1, 100)
    if check == 1:
        await shitpost(message)

# Split parameter into top and bottom text


def find_space(text):
    midpoint = int(len(text)/2)
    print(midpoint, text[midpoint])
    if text[midpoint] != ' ':
        for i in text[int(len(text)/2)::]:
            if i == ' ':
                return midpoint
            midpoint += 1
    return midpoint

# Handler to load in text and image to meme maker


async def shitpost(message):
    text = message.content[10::]
    midpoint = find_space(text)
    text1 = text[0:midpoint]
    text2 = text[midpoint+1::]
    numimages = os.listdir("src/meme_functionality/images")
    image = "src/meme_functionality/images/"+str(random.randint(1, len(numimages)-2))+'.png'
    sent = await message.channel.send("Making meme...")
    make_meme(text1, text2, image)
    await message.channel.send(file=discord.File('src/meme_functionality/images/output/output.png'))
    await sent.delete()

# Logic to generate meme


def make_meme(topString, bottomString, filename):
    img = Image.open(filename)
    imageSize = img.size
    # find biggest font size that works
    fontSize = int(imageSize[1]/5)
    font = ImageFont.truetype("C:/Windows/Fonts/Impact.ttf", fontSize)
    topTextSize = font.getsize(topString)
    bottomTextSize = font.getsize(bottomString)
    while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
        fontSize = fontSize - 1
        font = ImageFont.truetype("C:/Windows/Fonts/Impact.ttf", fontSize)
        topTextSize = font.getsize(topString)
        bottomTextSize = font.getsize(bottomString)
    # find top centered position for top text
    topTextPositionX = (imageSize[0]/2) - (topTextSize[0]/2)
    topTextPositionY = 0
    topTextPosition = (topTextPositionX, topTextPositionY)
    # find bottom centered position for bottom text
    bottomTextPositionX = (imageSize[0]/2) - (bottomTextSize[0]/2)
    bottomTextPositionY = imageSize[1] - bottomTextSize[1]
    bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)
    draw = ImageDraw.Draw(img)
    # draw outlines
    # there may be a better way
    outlineRange = int(fontSize/15)
    for x in range(-outlineRange, outlineRange+1):
        for y in range(-outlineRange, outlineRange+1):
            draw.text(
                (topTextPosition[0]+x, topTextPosition[1]+y), topString, (0, 0, 0), font=font)
            draw.text(
                (bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0, 0, 0), font=font)
    draw.text(topTextPosition, topString, (255, 255, 255), font=font)
    draw.text(bottomTextPosition, bottomString, (255, 255, 255), font=font)
    img.save("src/meme_functionality/images/output/output.png")


def get_upper(somedata):
    result = ''
    try:
        result = somedata.decode("utf-8").upper()
    except:
        result = somedata.upper()
    return result


def get_lower(somedata):
    result = ''
    try:
        result = somedata.decode("utf-8").lower()
    except:
        result = somedata.lower()
    return result
