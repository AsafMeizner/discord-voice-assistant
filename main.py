# discord imports
import discord
from discord import app_commands

# speech recognition imports
import speech_recognition as sr

# text to speech imports 
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 50)  

# set up intents
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# join vc command
@tree.command(name="join-vc", description="voice assistant joins the vc you are in")
async def join_vc(interation):
    # check if the user is in a vc
    if interation.user.voice and interation.user.voice.channel:
        # join the vc
        try:
            await interation.user.voice.channel.connect()
        except:
            await interation.response.send_message("Unable to join vc.", ephemeral=True)
        
        # if joined vc
        if interation.guild.voice_client and interation.guild.voice_client.is_connected():
            await interation.response.send_message("Joined vc.", ephemeral=True)
    
    # if the user is not in a vc
    else:
        # send a message saying that they are not in a vc
        await interation.response.send_message("You are not in a voice channel.", ephemeral=True)

# leave vc command
@tree.command(name="leave-vc", description="voice assistant leaves the vc you are in")
async def leave_vc(interation):
    if interation.guild.voice_client and interation.guild.voice_client.is_connected():
        await interation.guild.voice_client.disconnect()
        await interation.response.send_message("Left vc.", ephemeral=True)
    else:
        await interation.response.send_message("I am not connected to a voice channel.", ephemeral=True)

# text to speech command
@tree.command(name="say", description="voice assistant says what you want it to say")
async def say(interation, text: str):  # Add type annotation for the 'text' parameter
    if interation.guild.voice_client and interation.guild.voice_client.is_connected():
        engine.say(text)
        await interation.response.send_message('Said "' + text + '"', ephemeral=True)
        engine.runAndWait()
    else:
        try:
            await interation.user.voice.channel.connect()
            engine.say(text)
            await interation.response.send_message('Said "' + text + '"', ephemeral=True)
            engine.runAndWait()
        except:
            await interation.response.send_message("not connected to vc, and couldent connect.", ephemeral=True)

# on start event
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")
    await client.change_presence(activity=discord.Game(name="/help"))

# run bot
from dis_token import token
client.run(token)