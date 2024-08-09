"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""

from datetime import date
import time
from utils.CreateMovie import CreateMovie, GetDaySuffix
from utils.RedditBot import RedditBot
from utils.upload_video import upload_video

#Create Reddit Data Bot
redditbot = RedditBot()
counter = 1

# Leave if you want to run it 24/7
while counter < 100:

    # Gets our new posts pass if image related subs. Default is memes
    posts = redditbot.get_posts("dankmemes")

    # Create folder if it doesn't exist
    redditbot.create_data_folder()

    # Go through posts and find 5 that will work for us.
    for post in posts:
        redditbot.save_image(post)

    # Wanted a date in my titles so added this helper
    DAY = date.today().strftime("%d")
    DAY = str(int(DAY)) + GetDaySuffix(int(DAY))
    dt_string = date.today().strftime("%A %B") + f" {DAY}"

    # Save images locally
    for post in redditbot.post_data:
        redditbot.save_image(post)

    if redditbot.post_data and any(post['image_path'] for post in redditbot.post_data):
        CreateMovie.CreateMP4(redditbot.post_data, counter)
        #break
    else:
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("!  No valid images to create a video.  !")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")

    # Video info for YouTube.
    # This example uses the first post title.
    # video_data = {
    #         "file": f"output-{counter}.mp4",
    #         "title": f"{redditbot.post_data[0]['title']} - Dankest memes and comments {dt_string}!",
    #         "description": "#shorts\nGiving you the hottest memes of the day with funny comments!",
    #         "keywords":"meme,reddit,Dankestmemes",
    #         "privacyStatus":"public"
    # }

    # print(video_data["title"])
    # print("Posting Video in 5 minutes...")
    counter += 1
    #time.sleep(60 * 5)
    #upload_video(video_data)

    # Sleep until ready to post another video!
    #time.sleep(60 * 60 * 24 - 1)
