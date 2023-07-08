import discord
import speech_recognition as sr
from discord.ext import commands

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='ok discord ', intents=intents)
recognizer = sr.Recognizer()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and member.id != bot.user.id:
        if after.channel.name == 'Voice Channel Name':
            if after.channel != before.channel:
                await after.channel.connect()

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
        voice_channel = None
        for channel in bot.voice_clients:
            if message.author in channel.members:
                voice_channel = channel
                break

        if voice_channel:
            audio = await message.attachments[0].read()
            try:
                with sr.AudioFile(audio) as source:
                    audio_data = recognizer.record(source)
                    command = recognizer.recognize_google(audio_data)
                    await bot.process_commands(await bot.get_context(message))
            except sr.UnknownValueError:
                await message.channel.send("I'm sorry, I couldn't understand your command.")
            except sr.RequestError:
                await message.channel.send("I'm sorry, there was an issue processing your command.")
        else:
            await message.channel.send("Please join a voice channel first.")

    await bot.process_commands(message)


from dis_token import token
bot.run(token)