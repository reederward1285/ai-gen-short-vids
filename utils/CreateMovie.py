from moviepy.editor import *
import random
import os
from PIL import Image as PILImage


dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def GetDaySuffix(day):
    if day == 1 or day == 21 or day == 31:
        return "st"
    elif day == 2 or day == 22:
        return "nd"
    elif day == 3 or day == 23:
        return "rd"
    else:
        return "th"

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
music_path = os.path.join(dir_path, "Music/")

def add_return_comment(comment):
    need_return = 30
    new_comment = ""
    return_added = 0
    return_added += comment.count('\n')
    for i, letter in enumerate(comment):
        if i > need_return and letter == " ":
            letter = "\n"
            need_return += 30
            return_added += 1
        new_comment += letter
    return new_comment, return_added
        

class CreateMovie():

    @classmethod
    def CreateMP4(cls, post_data):
        image_paths = [post['image_path'] for post in post_data if post['image_path']]
        
        if not image_paths:
            print("No valid image paths found")
            return
        
        # Check if all images are the same size
        sizes = []
        for image_path in image_paths:
            with PILImage.open(image_path) as img:
                sizes.append(img.size)
        
        # Determine the size to use
        if len(set(sizes)) > 1:
            print("Warning: Not all images are the same size. Resizing images.")
            standard_size = max(sizes, key=lambda x: x[0] * x[1])  # Use the largest image size as the standard
            for path in image_paths:
                with PILImage.open(path) as img:
                    if img.size != standard_size:
                        img = img.resize(standard_size, PILImage.ANTIALIAS)
                        img.save(path)
        
        # Create video clip
        clip = ImageSequenceClip(image_paths, durations=[12]*len(image_paths))
        clip.write_videofile('output.mp4', fps=24)

if __name__ == '__main__':
    print(TextClip.list('color'))