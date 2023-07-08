import discord
import speech_recognition as sr
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='ok discord ', intents=intents)
recognizer = sr.Recognizer()

listening = False

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    global listening
    if after.channel and member.id != bot.user.id:
        if after.channel.name == 'Voice Channel Name':
            if after.channel != before.channel:
                await after.channel.connect()
                listening = True

@bot.command()
async def mute(ctx, member: discord.Member):
    if ctx.author.voice and ctx.author.voice.channel:
        if ctx.author.voice.channel.permissions_for(ctx.author).mute_members:
            if ctx.voice_client and ctx.voice_client.is_connected():
                await member.edit(mute=True)
                await ctx.send(f'{member.display_name} has been muted.')
            else:
                await ctx.send('I am not connected to a voice channel.')
        else:
            await ctx.send('You do not have the permission to mute members.')
    else:
        await ctx.send('You are not in a voice channel.')

@bot.command()
async def unmute(ctx, member: discord.Member):
    if ctx.author.voice and ctx.author.voice.channel:
        if ctx.author.voice.channel.permissions_for(ctx.author).mute_members:
            if ctx.voice_client and ctx.voice_client.is_connected():
                await member.edit(mute=False)
                await ctx.send(f'{member.display_name} has been unmuted.')
            else:
                await ctx.send('I am not connected to a voice channel.')
        else:
            await ctx.send('You do not have the permission to mute members.')
    else:
        await ctx.send('You are not in a voice channel.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('ok discord'):
        global listening
        listening = True

    await bot.process_commands(message)

def process_audio(audio):
    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            command = recognizer.recognize_google(audio_data)
            if command == 'ok discord':
                global listening
                listening = True
    except sr.UnknownValueError:
        pass
    except sr.RequestError:
        pass

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and member.id != bot.user.id:
        if after.channel.name == 'Voice Channel Name':
            if after.channel != before.channel:
                await after.channel.connect()
                while True:
                    global listening
                    if listening:
                        audio = await bot.voice_clients[0].record_and_save()
                        process_audio(audio)
                        listening = False


from dis_token import token
bot.run(token)