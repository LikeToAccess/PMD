from datetime import datetime
import os
import sys
# from threading import Thread
from multiprocessing.pool import ThreadPool
import discord
import youtube_dl
import config as cfg
from discord.ext import commands, tasks
import media
import download


async def log(ctx, authenticated, filename="log.txt"):
	if not authenticated:
		await ctx.message.delete()
		await ctx.send(f"*{ctx.author}*, is not in the allowed users list!\nThis event has been logged.")
	authenticated = "FAILED to execute" if not authenticated else "SUCCESFULLY executed"
	data = ctx.message.content
	data = f"[{datetime.now()}]{ctx.message.author} :: {authenticated} \"{data}\"\n"
	print(data)
	media.append_file(filename, data)

async def check_perms(ctx):
	author = ctx.message.author
	if str(author.id) in allowed_users:
		log(ctx, True)
		return True
	await log(ctx, False)
	return False


pool = ThreadPool(processes=1)
credentials = media.read_file("credentials.md", filter=True)
token = credentials[0]
allowed_users = credentials[1:]
channel_id = {
	"commands": 776367990560129066,
	"log": 776354053222826004,
}
bot = commands.Bot(command_prefix=
	[
		"!",
		"`",
		"~",
		"-",
		"please "
	],
	help_command=None, case_insensitive=True)


async def send(msg, channel="commands", silent=True):
	channel = bot.get_channel(channel_id[channel])
	await channel.send(msg)
	if not silent: print(msg)

@bot.listen("on_message")
async def on_message(message):
	if message.content.startswith("https://"):
		await send("Testing link...", silent=False)
		if "--res=" in message.content:
			forced_resolution = message.content.split("--res=")[1]
			cfg.write_attempts(int(forced_resolution))
		threaded_download = pool.apply_async(download.download, (message.content,))
		result = threaded_download.get()
		# print(f"DEBUG: result: {result}\nDEBUG: threaded_download: {threaded_download}")
		# # result = download(message.content)
		# if result:
		# 	send(result)
		# 	print("DEBUG: Sent result from bot.py to discord")
		# else: await send("FAILED download!")

@bot.event
async def on_ready():
	try:
		if sys.argv[1]:
			await send(" ".join(sys.argv[1:]))
			sys.exit(0)
	except IndexError: pass
	check_logs.start()
	print(f"{bot.user} successfuly connected!")
	await set_status("Free Movies on Plex!", discord.Status.online)

async def set_status(activity, status=discord.Status.online):
	await bot.change_presence(status=status, activity=discord.Game(activity))

@tasks.loop(seconds=5)
async def check_logs():
	log_data = media.read_file("log.txt", filter=True)
	for message in log_data:
		await send(message)
	media.write_file("log.txt", "### Beginning of message buffer from server ###\n")

@bot.command()
async def play(ctx, url : str):
	await join(ctx)
	home = os.getcwd()
	voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	ydl_opts = {
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "64",
		}],
	}
	os.chdir("MUSIC")
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([url])
	for file in os.listdir():
		if file.endswith(".mp3"):
			os.rename(file, "music.mp3")
	voice.play(discord.FFmpegPCMAudio("music.mp3"))
	os.chdir(home)
	await ctx.message.delete()
	print("Playing audio...")

@bot.command()
async def join(ctx):
	voice_channel = discord.utils.get(ctx.guild.voice_channels, name="▶voice-chat")
	await voice_channel.connect()
	# voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
	await ctx.message.delete()
	print("Joined \"▶voice-chat\".")

@bot.command()
async def leave(ctx):
	voice = discord.utils.get(bot.voice_clients)
	await voice.disconnect()
	await ctx.message.delete()
	print("Left \"▶voice-chat\".")

@bot.command()
async def pause(ctx):
	voice = discord.utils.get(bot.voice_clients)
	voice.pause()
	await ctx.message.delete()
	print("Paused audio.")

@bot.command()
async def resume(ctx):
	voice = discord.utils.get(bot.voice_clients)
	voice.resume()
	await ctx.message.delete()
	print("Unpaused audio.")

@bot.command()
async def stop(ctx):
	voice = discord.utils.get(bot.voice_clients)
	voice.stop()
	await ctx.message.delete()
	print("Stopped audio.")


def run():
	return bot.run(token)


if __name__ == "__main__":
	run()