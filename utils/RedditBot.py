from datetime import date
import os
import praw
from dotenv import load_dotenv
import requests
import json
from PIL import Image
from io import BytesIO

load_dotenv()


class RedditBot():

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('client_id'),
            client_secret=os.getenv('client_secret'),
            user_agent=os.getenv('user_agent'),
        )

        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_path = os.path.join(dir_path, "data/")
        self.post_data = []
        self.already_posted = []

        #   Check for a posted_already.json file
        self.posted_already_path = os.path.join(
            self.data_path, "posted_already.json")
        if os.path.isfile(self.posted_already_path):
            print("Loading posted_already.json from data folder.")
            with open(self.posted_already_path, "r") as file:
                self.already_posted = json.load(file)

    def get_posts(self, sub="memes"):
        self.post_data = []
        subreddit = self.reddit.subreddit(sub)
        posts = []
        for submission in subreddit.top("day", limit=3):
            if submission.stickied:
                print("Mod Post")
            else:
                # Create a dictionary to store the required data
                post_data = {
                    "id": submission.id,
                    "title": submission.title,
                    "image_path": self.get_image_url(submission),  # Get actual image URL
                    "Best_comment": submission.comments[0].body if submission.comments else "No comments",
                    "best_reply": "MIA"  # Set a default or extract as needed
                }
                print("added post to post_data: " + str(post_data))
                posts.append(post_data)
        
        self.post_data = posts  # Update the class attribute
        print("resulting post_data is " + str(self.post_data))
        return posts

    def get_image_url(self, submission):
        # Check if submission has a direct image URL
        if submission.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return submission.url  # Direct image URL
        elif hasattr(submission, 'media') and submission.media is not None:
            return submission.media['oembed']['thumbnail_url']  # Use thumbnail if available
        return None  # Return None if no valid image found

    def create_data_folder(self):
        today = date.today()
        dt_string = today.strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        check_folder = os.path.isdir(data_folder_path)
        # If folder doesn't exist, then create it.
        if not check_folder:
            os.makedirs(data_folder_path)

    def download_image(self, url, save_path):
        if not url:
            print("URL is empty or None")
            return None
        
        if not url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"URL does not point to an image: {url}")
            return None
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.save(save_path)
            return save_path
        except Exception as e:
            print(f"Error downloading image from {url}: {e}")
            return None



    def save_image(self, post, scale=(720, 1280)):
        image_url = post['image_path']
        if not image_url:
            print(f"No image URL provided for post ID {post['id']}")
            return

        local_path = os.path.join('images', f"{post['id']}.jpg")
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        local_image_path = self.download_image(image_url, local_path)

        if local_image_path:
            post['image_path'] = local_image_path
        else:
            print(f"Failed to download image from {image_url}")

