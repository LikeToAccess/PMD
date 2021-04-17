# TODO
Todo list for the project

## Will Do:
 * [ ] Limit simultanious downloads on the server
 * [ ] Send feedback on the overall progress of downloads back to the client
 * [x] Create a robust server to handle multiple client connections
 * [ ] Fix *client.py* to not be so bad
 * [x] Automatically download files with HTTP GET requests
 * [ ] Set up *server.py* as the server-side for active deployment
 * [ ] Create a binary executable for the client
 * [ ] If the movie failed to download, lower the resolution and try again
 * [ ] Integrate the client into the Discord bot for contributers to have easy access
 	* Networking is not needed as both programs will be running on the same system
 * [ ] Prevent the client from connecting unless their Discord can be verified
 	* The bot will DM a one-time code to authenticate the Discord tag entered is real and is permitted to connect
 	* There will also be an administrator override password
 * [ ] Credit the discord user who uploaded the movie in the *#▶new-media* channel
 	* Also show the contributer of the month in *#▶announcements*
 	* Assign a score/reward to a user for uploading a movie
 		* Scores will be used for later
 		* Add the propper scores to people who have uploaded prior to this functionality being implemented
 * [ ] Fully merge this project with the *Plex* Discord bot project
 	* The name will be changed to *Plex Bot* for everything

## Experimental Ideas:
 * [ ] Create a hotkey system to grab the link directly from the clipboard
 * [ ] Create a proxy to intercept the GET requests and forward the links to the server
