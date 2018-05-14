#=============================================================
#PRIDE BOT 1.1
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

#i made this one - it's ~*~local~*~
import dictbuilder

#IMPORTANT VARIABLES ============================================================
client_token = '' #<-------- put your token here!
pridebot = Bot(command_prefix = "!", pm_help = True)
pride_flags_dictionary = {} #built on startup

#temp variables for logging who called what
msg = None
caller = None

#THE HELP PROMPT ===============================================================
help_prompt = """
PRIDE BOT 1.1
by sympolite


COMMANDS:

(Commands are listed like "!command parameter [attachment]".)

!helpme - DMs you this prompt.

!flags - Returns a list of flags.

!prideflag flag [transparent PNG file] - Superimposes the PNG file onto a 1000x1000 pride flag
of your choice. See below for a list of flags, or call !flags.


"""


#HELPER FUCNTIONS ==============================================================

def get_flag_help():
    flags_prompt = ""
    try:
        with open('flaglist.txt', 'r') as flist:
            for line in flist:
                flags_prompt = flags_prompt + line
    except FileNotFoundError:
        flags_prompt = "WARNING: the administrator of this bot has not created \"flaglist.txt\", or it is missing!"
    return flags_prompt

def random_name():
    random_name = ""
    #create a random image name
    for i in range(8):
        random_name += chr(random.randint(ord('a'),ord('z')))
    return random_name

def save_image(pic_url):
    filetype = pic_url[-4:].lower()
    temp_file = 'temp/' + random_name() + filetype
    with open(temp_file, 'wb') as handle:
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return temp_file

def autocrop(base_image):
    base_image_data = np.asarray(base_image)
    #get alpha channel of all pixels (R = 0, G = 1, B = 2, A = 3)
    image_data_bw = base_image_data[:,:,3] 
    #get all non-transparent pixels (alpha > 0)
    non_empty_columns = np.where(image_data_bw.max(axis=0)>0)[0]
    non_empty_rows = np.where(image_data_bw.max(axis=1)>0)[0]
    if not (non_empty_columns.any() and non_empty_rows.any()):
        return None
    cropBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))  
    im_data = base_image_data[cropBox[0]:cropBox[1]+1, cropBox[2]:cropBox[3]+1 , :]
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

@pridebot.command() #to do: make this less monolithic and procedural
async def prideflag(arg):
    arg = arg.lower() 
    #temporay copy of the message
    _msg = msg
    #check the goods
    if arg not in pride_flags_dictionary:
        await pridebot.say(f"ERROR: `{arg}` is currently not a valid pride flag name.")
        return
    if not _msg.attachments:
        await pridebot.say("ERROR: There is no attached image.")
        return
    pic_url = _msg.attachments[0]['url']
    filetype = pic_url[-4:].lower()
    print(f'filetype = {filetype}')
    if filetype != ".png":
        await pridebot.say("ERROR: the attached image is not a PNG file.")
        return
    #and now, we save the image
    temp_image = save_image(pic_url)
    await pridebot.send_typing(_msg.channel)
    base = Image.open(f'flags/{pride_flags_dictionary[arg]}.png').convert('RGBA')
    top = Image.open(temp_image).convert('RGBA')
    copy_base = base.copy()
    copy_top = top.copy()
    #autocrop and see if the image isn't blank
    cropped_top = autocrop(copy_top)
    if cropped_top is None:
        await pridebot.say("ERROR: The image was blank.")
        os.remove(os.path.join(os.getcwd(),final_file))
        os.remove(os.path.join(os.getcwd(),temp_image))
        return
    #get dims
    width, height = cropped_top.size
    flag_w, flag_h = copy_base.size
    min_dim = min(flag_w/width, flag_h/height)
    new_w = int(width * min_dim)
    new_h = int(height * min_dim)
    copy_top_resized = cropped_top.resize((new_w, new_h),resample=1)
    #create a blank and paste the image onto it for compositing
    blank = Image.new('RGBA', (flag_w,flag_h), (0,0,0,0))
    xpos = (flag_w-new_w)//2
    ypos = (flag_h-new_h)//2
    blank.paste(copy_top_resized, (xpos, ypos))
    #and voila! the pride flag is made
    final_image = Image.alpha_composite(copy_base, blank)
    final_file = f'temp/{arg}_{random_name()}.png'
    final_image.save(final_file)
    await pridebot.send_file(_msg.channel, final_file)
    os.remove(os.path.join(os.getcwd(),final_file))
    os.remove(os.path.join(os.getcwd(),temp_image))

#================================================================================================
#THE REAL SHISH
#================================================================================================    
print("PRIDE BOT v1.0\nby sympolite\ngithub.com/sympolite\n...")
try:
    os.makedirs(os.path.join(os.getcwd(),"temp"))
except:
    print("Temp folder exists!")
if os.path.isdir(os.path.join(os.getcwd(),"flags")):
    try:
        pride_flags_dictionary = dictbuilder.build_dict('config.txt')
        print('Dictionary built!')
        flags_prompt = get_flag_help()
        help_prompt += flags_prompt
        print('Flags prompt created!')
        print('Starting bot...')
        pridebot.run(client_token)
    except Exception as e:
        print(str(e))
        sys.exit(1)
else:
    print("FATAL ERROR: /flags folder is missing!")
    sys.exit(1)
