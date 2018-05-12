#=============================================================
#PRIDE BOT 1.0
#by sympolite
#github.com/sympolite
#femme pride flag by noodle.tumblr.com
#=============================================================

#core modules
import random
import time
import os
import io

#make sure to get these using pip
import discord
from discord.ext.commands import Bot
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont

client_token = '' #<-------- put your token here!
pridebot = Bot(command_prefix = "!", pm_help = True)

#temp variables for logging who called what
msg = None
caller = None

#width and/or height of pride flags
base_dim = 1000

#THE HELP PROMPT ===============================================================

flags_prompt = """
FLAGS:
(Flags are listed as "valid, list, of, words - Flag")

les, lez, lesbian - Lesbian
gay - Gay
bi, bisexual - Bisexual
pan, pansexual - Pansexual
ace, asexual - Asexual

trans, transgender, transsexual - Transgender
agender - Agender
gq, genderqueer - Genderqueer
nonbinary, nb, enby - Nonbinary

bear - Bear Pride
twink - Twink Pride
butch - Butch Pride
femme - Femme Pride (designed by http://noodle.tumblr.com)
"""

help_prompt = """
PRIDE BOT 1.0
by sympolite


COMMANDS:

(Commands are listed like "!command parameter [attachment]".)

!help - DMs you this prompt.

!flags - Returns a list of flags.

!prideflag flag [transparent PNG file] - Superimposes the PNG file onto a 1000x1000 pride flag
of your choice. See below for a list of flags, or call !flags.


""" + flags_prompt

#THE DICTIONARY ================================================================

pride_flags_dictionary = {"gay":"gay.png",
                          "lesbian": "lesbian.png",
                          "les": "lesbian.png",
                          "lez": "lesbian.png",
                          "bi": "bi.png",
                          "bisexual": "bi.png",
                          "pan": "pan.png",
                          "pansexual": "pan.png",
                          "ace": "ace.png",
                          "asexual": "ace.png",
                          "agender": "agender.png",
                          "bear": "bear.png",
                          "twink": "twink.png",
                          "butch": "butch.png",
                          "femme": "femme.png",
                          "trans": "trans.png",
                          "transgender": "trans.png",
                          "transsexual": "trans.png",
                          "genderqueer": "genderqueer.png",
                          "gq": "genderqueer.png",
                          "nonbinary": "nonbinary.png",
                          "nb": "nonbinary.png",
                          "enby": "nonbinary.png"
                          }

#HELPER FUCNTIONS ==============================================================

def random_name():
    random_name = ""
    #create a random image name
    for i in range(8):
        random_name += chr(random.randint(ord('a'),ord('z')))
    return random_name

def save_image(pic_url):
    filetype = pic_url[-4:].lower()
    temp_file = 'temp/' + random_name() + filetype
    
    #save the image
    with open(temp_file, 'wb') as handle:
        #get image data from url
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print(response)
        #get ALL the data
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return temp_file

    
def autocrop(base_image):
    #convert to array
    base_image_data = np.asarray(base_image)
    
    #get alpha channel of all pixels (R = 0, G = 1, B = 2, A = 3)
    image_data_bw = base_image_data[:,:,3] 

    #get all non-transparent pixels (alpha > 0)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]

    #return None if the image is empty
    if not (non_empty_columns.any() and non_empty_rows.any()):
        return None
    
    #create a bounding box
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

    #crop the image proper    
    im_data = base_image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]

    #and create it!
    autocropped_image = Image.fromarray(im_data)
    return autocropped_image

#EVENTS========================================================================
@pridebot.event
async def on_ready():
    print('Ready!')
    
@pridebot.event
async def on_message(message):
    await pridebot.change_presence(game=discord.Game(name='!helpme'))
    global msg
    msg = message
    await pridebot.process_commands(msg)

@pridebot.event
async def on_message_edit(before, after): 
    global msg
    msg = after
    await pridebot.process_commands(msg)

#COMMANDS=======================================================================

@pridebot.command()
async def helpme():
    _msg = msg
    await pridebot.send_message(_msg.author, content=f"```{help_prompt}```")

@pridebot.command()
async def flags():
    _msg = msg
    await pridebot.say(f"```{flags_prompt}```")

@pridebot.command()
async def prideflag(arg):
    arg = arg.lower() 
    #temporay copy of the message
    _msg = msg

    #check the dict
    if arg not in pride_flags_dictionary:
        await pridebot.say(f"ERROR: `{arg}` is currently not a valid pride flag name.")
        return

    #check if a pic is attached
    if not _msg.attachments:
        await pridebot.say("ERROR: There is no attached image.")
        return
    
    #check if a pic is a PNG file
    pic_url = _msg.attachments[0]['url']
    filetype = pic_url[-4:].lower()
    print(f'filetype = {filetype}')
    if filetype != ".png":
        await pridebot.say("ERROR: the attached image is not a PNG file.")
        return

    #save the image! (duh)
    temp_image = save_image(pic_url)
    await pridebot.send_typing(_msg.channel)

    #open the flag and the given PNG
    base = Image.open(f'flags/{pride_flags_dictionary[arg]}').convert('RGBA')
    top = Image.open(temp_image).convert('RGBA')

    #create copies
    copy_base = base.copy()
    copy_top = top.copy()

    #autocrop the top! (remove extraneous transparent space)
    cropped_top = autocrop(copy_top)

    #get the dims of the PNG
    width, height = cropped_top.size
    #get smallest dimension
    min_dim = min(base_dim/width, base_dim/height)
    #resize so the smallest dim is 1000px
    new_w = int(width * min_dim)
    new_h = int(height * min_dim)
    #and resize!
    copy_top_resized = cropped_top.resize((new_w, new_h),resample=1)

    #create a blank image to paste the PNG onto
    blank = Image.new('RGBA', (base_dim,base_dim), (0,0,0,0))
    #center the given PNG
    xpos = (base_dim-new_w)//2
    ypos = (base_dim-new_h)//2
    #and paste!
    blank.paste(copy_top_resized, (xpos, ypos))
    
    #put the PNG (with added blank space so the composite works)
    #onto the flag image
    final_image = Image.alpha_composite(copy_base, blank)
    final_file = f'temp/{arg}_{random_name()}.png'
    final_image.save(final_file)
    await pridebot.send_file(_msg.channel, final_file)
    os.remove(os.path.join(os.getcwd(),final_file))
    os.remove(os.path.join(os.getcwd(),temp_image))

#================================================================================================
print("PRIDE BOT v1.0\nby sympolite\ngithub.com/sympolite\n...")
try:
    os.makedirs(os.path.join(os.getcwd(),"temp"))
except:
    print("Temp folder exists!")
if os.path.isdir(os.path.join(os.getcwd(),"flags")):
    pridebot.run(client_token)
else:
    print("FATAL ERROR: /flags folder is missing!")
