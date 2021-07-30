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
scraper = Scraper()
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


#                    |
#  Discord Functions |
#                    V

@bot.event
async def on_ready():
	check_logs.start()
	print(f"{bot.user} successfuly connected!")
	await set_status("Free Movies on Plex!", discord.Status.online)
	# await create_embed({'data-filmname': "Zack Snyder's Justice League (Black and White)", 'data-year': '2021', 'data-imdb': 'IMDb: 8.1', 'data-duration': '242 min', 'data-country': 'United Kingdom', 'data-genre': 'Action, Adventure, Fantasy, Sci-Fi', 'data-descript': "Determined to ensure Superman's ultimate sacrifice was not in vain, Bruce Wayne aligns forces with Diana Prince with plans to recruit a team of met...", "img":"https://static.gomovies-online.cam/dist/img/C97to1aFchTRotSn63m3yc6k-oA7ou6anY3ruU8Lf2WevlTvJjQks5i_z5fTnadgcYV7z9aVPQcKUVsAxMzkDleaTjfFbze08mdub0ZTXuq3y0XxXiUGmfEQFgfeMfN-.jpg"})

@bot.listen("on_message")
async def on_message(message):
	if not message.content.startswith("https://gomovies-online."): return
	if message.channel.id != channel_id["commands"]: return
	if message.author == bot.user: return

	await send("Testing link...", silent=False)
	if "--res=" in message.content:
		forced_resolution = message.content.split("--res=")[1]
		cfg.write_attempts(int(forced_resolution))
	author = message.author
	link = message.content
	run_download(link, author.id)
	# threaded_download = Thread(target=download.download, args=(link,author))
	# threaded_download.start()

@tasks.loop(seconds=0.5)
async def check_logs(filename="log.txt"):
	log_data = media.read_file(filename, filter=True)
	media.write_file(filename, "### Beginning of message buffer from server ###\n")
	if log_data:
		message = "\n".join(log_data)
		# print(message)
		if "--channel=" in message:
			message = message.split("--channel=")
			await send(message[0], channel=message[1])
		elif "--embed" in message:
			metadata = eval(message.replace("--embed",""))
			await create_embed(metadata)
		else:
			await send(message)
		# for message in log_data:
		# 	if "--channel=" in message:
		# 		message = message.split(" --channel=")
		# 		await send(message[0], channel=message[1])
		# 	else:
		# 		await send(message)


#                   |
#  Discord Commands |
#                   V

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

# # TODO
# @bot.command()
# async def cancel(ctx, *filename):
# 	#!cancel Star Wars The Bad Batch - S01e01 - Aftermath
# 	if len(filename) > 1: filename = " ".join(filename)

@bot.command(aliases=["add", "download"])
async def download_first_result(ctx, *movie_name):
	movie_name = " ".join(movie_name)
	author = ctx.author.id
	# print(movie_name)
	# TODO: make this multithreaded
	if "https://gomovies-online." in movie_name:
		await send("Downloading via direct link...")
		url = scraper.get_download_link(movie_name)  # This would be a link not a query
	else:
		await send("Searching for matches...")
		url = scraper.download_first_from_search(movie_name)  # Searches using a movie title

	if url:
		await send("Link found, downloading starting...")
		run_download(url.get_attribute("src"), author)  # If there were any results found, then download
	else:
		await send("**ERROR**: No search results found!")

@bot.command()
async def search(ctx, *search_query):
	search_query = " ".join(search_query)
	author = ctx.author.id
	await send("Searching for matches...")
	# url = scraper.download_first_from_search(movie_name)  # Searches using a movie title
	if search_query:
		results, metadata = scraper.search(
			"https://gomovies-online.cam/search/" + \
			"-".join(search_query.split())
		)
		if results:
			print(metadata)
			for description in metadata:
				await create_embed(description)
		# await send("Link found, downloading starting...")
		# run_download(url.get_attribute("src"), author)  # If there were any results found, then download

@bot.command()
async def react(ctx):
	await ctx.message.add_reaction("\U0001F44D")

@bot.command()
async def solve(ctx, captcha_solution):
	await ctx.message.delete()
	filename = "solved_captcha.txt"
	media.write_file(filename, captcha_solution)
	await ctx.send("Attempting captcha solve...")


#                  |
#  Async Functions |
#                  V

async def create_embed(metadata, color=0xcbaf2f, channel="commands"):
	# description = (
	# 	message["data-year"],
	# 	message["data-imdb"],
	# 	message["data-duration"],
	# 	"Country: " + message["data-country"],
	# 	message["data-genre"],
	# 	message["data-descript"]
	# )
	# embed = discord.Embed(
	# 	title=title,
	# 	description=description,
	# 	color=color
	# )

	# embed.set_thumbnail(url=thumbnail_url)
	# print(metadata)
	embed = discord.Embed(
			title=metadata["data-filmname"],
			description="\U0000200B",
			colour=color
		)

	embed.set_footer(text=metadata["data-descript"])
	# embed.set_image(url="https://cdn.discordapp.com/attachments/520265639680671747/533389224913797122/rtgang.jpeg")
	embed.set_thumbnail(url=metadata["img"])
	# embed.set_author(name="Author Name", icon_url="https://cdn.discordapp.com/attachments/520265639680671747/533389224913797122/rtgang.jpeg")
	embed.add_field(name="\U0001F4C5", value=metadata["data-year"], inline=True)
	embed.add_field(name="IMDb", value=metadata["data-imdb"], inline=True)
	embed.add_field(name="\U0001F554", value=metadata["data-duration"], inline=True)
	await bot.get_channel(channel_id[channel]).send(embed=embed)

async def send(msg, channel="commands", silent=True):
	channel = bot.get_channel(channel_id[channel])
	image = False
	if "--file=" in msg: msg = msg.split("--file=")
	if not image: await channel.send(msg)
	else:
		await channel.send(file=discord.File(msg[1]))
		await channel.send(msg[0].strip())
	if not silent: print(msg)

async def set_status(activity, status=discord.Status.online):
	await bot.change_presence(status=status, activity=discord.Game(activity))


#            |
#  Functions |
#            V

def run_download(link, author):
	threaded_download = Thread(target=download.download, args=(link,author))
	threaded_download.start()

def run():
	return bot.run(token)


if __name__ == "__main__":
	run()
