from src import discord
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import os
import requests
import json
import shutil

#resize image
def resize(image):
    img = Image.open(image)
    img.save("src/meme_functionality/images/temp.jpg",optimize = True, quality = 10)
#Fetch memes from a cursed image sub-reddit to use with our meme making function
async def fetch_meme(message):
    url_list= ['https://www.reddit.com/r/nocontextpics.json','https://www.reddit.com/r/blursedimages.json']
    response_API = requests.get(random.choice(url_list), headers={'User-agent': 'Based Bot 1.0'})
    if not response_API.ok:
        print("Error", response_API.status_code)
        await message.channel.send("Slow down on the memes buddy")
        return "error"
    data = response_API.text
    parsed_data= json.loads(data)
    image_url = parsed_data["data"]["children"][random.randint(2,len(parsed_data["data"]["children"])-1)]["data"]["url_overridden_by_dest"]
    resp = requests.get(image_url, stream=True)
    local_file = open('src/meme_functionality/images/temp.jpg', 'wb')
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    print(is_image_greater_then_8_MB())
    if is_image_greater_then_8_MB():
        print("Image too big, getting another")
        fetch_meme(message)
        
#Check and see if gotten image is >8MB
def is_image_greater_then_8_MB():
    file_path = 'src/meme_functionality/images/temp.jpg'
    file_size = os.path.getsize(file_path)
    print(file_size/1024**2)
    if file_size/1024**2 > 8:
        return True
    return False
# Random chance that any message sent will turn into a meme


async def roulette(message):
    check = random.randint(1, 100)
    if check == 1:
        await shitpost(message, was_random=True)

# Split parameter into top and bottom text


def find_space(text):
    midpoint = int(len(text)/2)
    if text[midpoint] != ' ':
        for i in text[int(len(text)/2)::]:
            if i == ' ':
                return midpoint
            midpoint += 1
    return midpoint

# Handler to load in text and image to meme maker


async def shitpost(message, was_random):
    print("Initaiting Shitposting Sequence")
    flag = await fetch_meme(message)
    print("Meme has been fetched")
    if flag == "error":
        return
    if not was_random:
        text = message.content[10::]
    else:
        text = message.content
    midpoint = find_space(text)
    text1 = text[0:midpoint]
    text2 = text[midpoint+1::]
    numimages = os.listdir("src/meme_functionality/images")
    image = "src/meme_functionality/images/temp.jpg"
    sent = await message.channel.send("Making meme...")
    make_meme(text1, text2, image)
    print("Meme has been made")
    await message.channel.send(file=discord.File('src/meme_functionality/images/output/output.jpg'))
    await sent.delete()

# Logic to generate meme
def make_meme(topString, bottomString, filename):
    resize(filename)
    print("Meme is being made")
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
    img.save("src/meme_functionality/images/output/output.jpg", optimize = True, quality = 30)


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
