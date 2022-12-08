# -*- coding: utf-8 -*-
# filename          : bot.py
# description       : Discord bot interface for interacting with the server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 08-01-2021
# version           : v2.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import time
from threading import Thread
import discord
from requests.exceptions import MissingSchema
from discord.ext import commands, tasks
from scraper import Scraper
from errors import NoResults
# import config as cfg
import media
import download


credentials = media.read_file("credentials.md", filter=True)
scraper = Scraper()
token = credentials[0]
allowed_users = credentials[1:]
intents = discord.Intents.default()
intents.message_content = True
channel_id = {
	"commands": 776367990560129066,
	"log": 776354053222826004,
	"spam": 780948981299150888,
}
bot = commands.Bot(command_prefix=
	[
		"beta ",
		"Beta ",
		"BETA ",
		"please ",
		"Please ",
		"PLEASE ",
		"pls ",
		"Pls ",
		"PLS ",
	],
	help_command=None, case_insensitive=True, intents=intents)


#                    |
#  Discord Functions |
#                    V

@bot.event
async def on_ready():
	check_logs.start()
	print(f"{bot.user} successfuly connected!")
	await set_status("Free Movies on Plex!", discord.Status.online)

@bot.listen("on_message")
async def on_message(message):
	if not message.content.startswith("https://gomovies-online."): return
	if message.channel.id != channel_id["commands"]: return
	if message.author == bot.user: return

	await send("Testing link...", silent=False)
	# if "--res=" in message.content:
	# 	forced_resolution = message.content.split("--res=")[1]
	# 	cfg.write_attempts(int(forced_resolution))
	author = message.author
	source_url = message.content
	download_queue = scraper.get_download_link(source_url)
	for data in download_queue:
		target_url, metadata, *_ = data
		run_download(target_url, metadata, author.id)

@tasks.loop(seconds=0.5)
async def check_logs(filename="log.txt"):
	log_data = media.read_file(filename, filter=True)
	if log_data:
		media.write_file(filename, "### Beginning of message buffer from server ###\n")

		bulk_message = []
		for message in log_data:
			if "--embed" in message:
				metadata = eval(message.replace("--embed",""))
				await create_embed(metadata)
			elif "--channel=" in message:
				message = message.split("--channel=")
				await send(message[0], channel=message[1])
			elif "--file" in message:
				await send(message)
			# elif "--res=" in message:
			# 	forced_resolution = message.split("--res=")[1]
			# 	cfg.write_attempts(int(forced_resolution))
			# 	bulk_message.append(message.split("--res=")[0])
			else:
				bulk_message.append(message)

		if bulk_message: await send("\n".join(bulk_message))





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
	author = user.display_name
	total_size = (
		f"{int(round(total_size, 0))} MB" if total_size < 2048 else f"{round(total_size/1024, 2)} GB"
	)
	await send(
		f"{author} has downloaded {len(movies)} movies/episodes totaling {total_size}."
	)

@bot.command(aliases=["add", "download"])
async def download_first_result(ctx, *movie_name):
	movie_name = " ".join(movie_name)
	author = ctx.author.id
	scraper.author = author
	if "https://gomovies-online." in movie_name:
		await send("Downloading via direct link...")
		download_queue = scraper.get_download_link(movie_name)  # This would be a link not a query
	else:
		await send("Searching for matches...")
		try:
			download_queue = scraper.download_first_from_search(movie_name)  # Searches using a movie title
		except NoResults:
			download_queue = None

	if download_queue:
		for data in download_queue:
			url, metadata, author = data
			if url:
				# If there were results and there is a valid URL, then download
				await send("Link found, downloading starting...")
				# print(f"DEBUG: {metadata}")
				await create_embed(metadata[list(metadata)[0]])
				run_download(url, metadata[list(metadata)[0]], author)
			else:
				await send("**ERROR**: No search results found!")
	else:
		await send("No results!", silent=False)

@bot.command()
async def search(ctx, *search_query):
	search_query = " ".join(search_query)
	author = ctx.author.id
	scraper.author = author
	start_time = time.time()
	if search_query:
		results, metadata = scraper.search(
			"https://gomovies-online.cam/search/" + \
			"-".join(search_query.split())
		)
		print(f"Finished scraping search results in {round(time.time()-start_time,2)} seconds!")

		if results and metadata:
			for description in metadata:
				# print(description)
				await create_embed(metadata[description])
		else:
			await send("**ERROR**: No search results found!")

@bot.command()
async def react(ctx):
	await ctx.message.add_reaction("\U0001F44D")

@bot.command(aliases=["status", "validate"])
async def validate_url(ctx, *url):
	url = " ".join(url)
	try:
		status_code = download.validate_url(url)[0]
		await send(f"Status for URL: {status_code}")
	except MissingSchema as error:
		await send(str(error))

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
	embed = discord.Embed(
			title=metadata["data-filmname"],
			description=metadata["data-genre"],
			color=color
		)

	embed.set_footer(text=metadata["data-descript"])
	embed.set_thumbnail(url=metadata["img"])
	embed.add_field(name="\U0001F4C5", value=metadata["data-year"], inline=True)
	embed.add_field(name="IMDb", value=metadata["data-imdb"], inline=True)
	embed.add_field(name="\U0001F554", value=metadata["data-duration"], inline=True)
	await bot.get_channel(channel_id[channel]).send(embed=embed)

async def send(msg, channel="commands", silent=True):
	channel = bot.get_channel(channel_id[channel])
	if "--file" in msg:
		msg = msg.split("--file=")
		print(f"DEBUG: msg contains \"--file\" and the filename is \"{msg[1]}\"")
		await channel.send(msg[0].strip())
		await channel.send(file=discord.File(msg[1]))
	else:
		await channel.send(msg)

	if not silent: print(msg)

async def set_status(activity, status=discord.Status.online):
	await bot.change_presence(status=status, activity=discord.Game(activity))


#            |
#  Functions |
#            V

def run_download(url, metadata, author):
	download_function = download.Download(url, metadata, author)
	threaded_download = Thread(target=download_function.run)
	threaded_download.start()

def run():
	return bot.run(token)


if __name__ == "__main__":
	run()
