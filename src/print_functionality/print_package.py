"""Functionality for all Nelson Net Printing functions"""
from discord.colour import Color
import requests
import discord
import cv2

async def fetch_status(ctx):
    """Fetch status of printer from octoprint then return as an embed"""
    headers = {'X-Api-Key':'B8E70612901844AD9A154E674B114B9B'}
    url = "http://10.0.0.138:8080/api/"
    jobdata = requests.get(url+'job', headers=headers).json()
    printerdata = requests.get(url+'printer', headers=headers).json()
    if(jobdata['state'] == "Paused"):
        color = discord.Color.from_rgb(255,255,0)
    elif(jobdata['state'] == "Printing"):
        color = discord.Color.green()
    else:
        color = discord.Color.red()
    get_image()
    embed = discord.Embed(
            title="Currently Printing: " + str(jobdata['job']['file']['name']),
            description="Nelson Net Printer is " + str(jobdata['state']),
            color=color)
    embed.add_field(name = "Progress",
                        value = str(int(jobdata['progress']['completion']) * 100) + "% finished")
    embed.add_field(name="Cost", value="$"+str(float((jobdata['job']['filament']['tool0']['length']) / 1000) * 0.06))
    embed.add_field(name = "Estimated Completion Time",
                        value = str(float(jobdata['progress']['printTimeLeft']/3600)) + " Hours")
    embed.add_field(name = "Current Running Time",
                        value = jobdata['progress']['printTime'])
    embed.add_field(name = "Extruder Temperature",
                        value = printerdata['temperature']['tool0']['actual'])
    await ctx.send(embed=embed)
    with open("image.jpg", "rb") as fh:
        f = discord.File(fh, filename="image.jpg")
    await ctx.send(file=f)

def get_image():
    stream = cv2.VideoCapture("http://10.0.0.138:8082")
    while(True):
        ret,frame = stream.read()
        cv2.imwrite("image.jpg", frame) 
        break
    





