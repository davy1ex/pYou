import os
from datetime import datetime
import subprocess
# import time

from pytube import YouTube
from pytube.exceptions import RegexMatchError

def isint(n):
    try:
        int(n)
        return True
    except:
        return False

def toMp3(filename):
    import moviepy.editor as mp
    clip = mp.VideoFileClip(filename).subclip(0, 20)
    clip.audio.write_audiofile(filename[:-3] + "mp3")

def download(link, only_audio=None):
    # if isint(link) == False:
    #     # pytube.YouTube(link)
    #     print("Yes, is link")
    # else:
    #     print("NO, try again")
    try:
        if only_audio != None:
            foundend_streams = YouTube(link).streams.filter(only_audio=True).all()
        else:
            foundend_streams = YouTube(link).streams.filter(file_extension="mp4").all()
        print("{} videos found, select...".format(len(foundend_streams)), "\n")
        # time.sleep(3)
        for index, video in enumerate(foundend_streams, 1):
            name = video.default_filename
            size = round(video.filesize / 1024 / 1024, 1)
            print(f"\t{index}. {name} {size} MB")
        parent_dir = os.path.join(os.getcwd(), "Downloads")
        #parent_dir = os.getcwd() + "/Downloads"
        index = int(input())        
        if isint(index) == True:            
            print("Download is start")
            os.mkdir(parent_dir)
            foundend_streams[index].download(parent_dir)
            name = foundend_streams[index].default_filename
            new_name = name[:-3] + "mp3"
            #new_filename = name[:-3] + "mp3"
            print("formating...")
            os.rename(os.path.join(os.getcwd(), "Downloads", name), os.path.join(os.getcwd(), "Downloads", new_name))
            # os.rename("./Donload/" + name, "./Donload/" + new_name)
            #subprocess.call(['ffmpeg', '-i',                # or subprocess.run (Python 3.5+)
            #    os.path.join(parent_dir, name),
            #    os.path.join(parent_dir, new_filename)
            #])
            print("Finished")
        else:
            print("Error: index is not int")
    except RegexMatchError:
        print("ERROR: The entered URL is incorrect")

if __name__ == "__main__":
    download(input("Input ULR: "))
