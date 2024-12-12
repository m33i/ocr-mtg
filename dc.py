import discord
from secret import token
from discord.ext import commands, voice_recv
import datetime
import ffmpeg
import os
import sys

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

discord.opus._load_default()


bot = commands.Bot(command_prefix=commands.when_mentioned, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")
    await connect_to_voice_channel(1287775798157115564) # channel id

async def connect_to_voice_channel(channel_id):
    channel = bot.get_channel(channel_id)
    if channel and isinstance(channel, discord.VoiceChannel):
        vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
        await bot.change_presence(status=discord.Status.online)
        print(f"connected to voice channel: {channel.name}")
        #   detect self video
    else:
        print("voice channel not found")

bot.run(token)