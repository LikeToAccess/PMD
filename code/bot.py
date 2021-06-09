# -*- coding: utf-8 -*-
# filename          : bot.py
# description       : Discord bot interface for interacting with the server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-04-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import os
from threading import Thread
import discord
import youtube_dl
from discord.ext import commands, tasks
from scraper import Scraper
import config as cfg
import media
import download


credentials = media.read_file("credentials.md", filter=True)
token = credentials[0]
allowed_users = credentials[1:]
channel_id = {
	"commands": 776367990560129066,
	"log": 776354053222826004,
	"spam": 780948981299150888,
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


@bot.event
async def on_ready():
	check_logs.start()
	print(f"{bot.user} successfuly connected!")
	await set_status("Free Movies on Plex!", discord.Status.online)

@bot.listen("on_message")
async def on_message(message):
	if message.content.startswith("https://") \
	and message.channel.id == channel_id["commands"] \
	and not "captcha?v=" in message.content:
		await send("Testing link...", silent=False)
		if "--res=" in message.content:
			forced_resolution = message.content.split("--res=")[1]
			cfg.write_attempts(int(forced_resolution))
		author = message.author.id
		link = message.content
		run_download(link, author)
		# threaded_download = Thread(target=download.download, args=(link,author))
		# threaded_download.start()

async def send(msg, channel="commands", silent=True):
	channel = bot.get_channel(channel_id[channel])
	image = False
	if "--file=" in msg: image = msg.split("=")[1]
	if not image: await channel.send(msg)
	else: await channel.send(file=discord.File(image))
	if not silent: print(msg)

async def set_status(activity, status=discord.Status.online):
	await bot.change_presence(status=status, activity=discord.Game(activity))

@tasks.loop(seconds=5)
async def check_logs():
	log_data = media.read_file("log.txt", filter=True)
	if log_data:
		for message in log_data:
			if "--channel=" in message:
				message = message.split(" --channel=")
				await send(message[0], channel=message[1])
			else:
				await send(message)
		media.write_file("log.txt", "### Beginning of message buffer from server ###\n")

@bot.command()
async def downloads(ctx, user: discord.User, *flags):
	total_size = 0  # This is in MB
	movies = []
	user_id = user.id
	lines = media.read_file(f"{user_id}.txt", filter=True)
	for line in lines:
		line = line.split("|")
		movies.append(line[0])
		total_size += float(line[2])
	if "--list" in flags:
		await send("{}".format("\n".join(movies)))
	await send(
		f"{user.display_name} has downloaded \
		{len(movies)} movies/episodes totaling \
		{round(total_size,0)} MB."
	)

# TODO
@bot.command()
async def cancel(ctx, *filename):
	#!cancel Star Wars The Bad Batch - S01e01 - Aftermath
	if len(filename) > 1: filename = " ".join(filename)

@bot.command(name="download", aliases=["add"])
async def search_and_download(ctx, *movie_name):
	if len(movie_name) > 1: movie_name = " ".join(movie_name)
	else: movie_name = movie_name[0]
	author = ctx.author.id
	scraper = Scraper("https://gomovies-online.cam/")
	print(movie_name)
	url = scraper.search(movie_name)
	if url:
		run_download(url, author)

@bot.command()
async def solve(ctx, captcha_solution):
	await ctx.message.delete()
	filename = "solved_captcha.txt"
	media.write_file(filename, captcha_solution)
	await ctx.send("Attempting captcha solve...")

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

def run_download(link, author):
	threaded_download = Thread(target=download.download, args=(link,author))
	threaded_download.start()

def run():
	return bot.run(token)


if __name__ == "__main__":
	run()
