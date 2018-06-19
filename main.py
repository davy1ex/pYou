# Почитай PEP8, сцуко. Сначала импортируются модули стандартной библиотеки,
# затем - сторонние пакеты. Последними идут модули собственного написания.
# отделяется всё это пустой строкой

import os
from datetime import datetime
from tkinter import *
from tkinter.scrolledtext import ScrolledText

from pytube import YouTube
from pytube.exceptions import RegexMatchError

from components.entry_with_placeholder import EntryWithPlaceholder
from helpers import bytes_to_human_readable


class GUI:
    DOWNLOAD_DIR = os.path.join(os.getcwd(), "/Downloads")

    def __init__(self, root):
        self.root = root
        self.root.title("pYou")

        # initialize frames
        # Вот тут 100% можно обойтись без трёх фреймов.
        self.header_frame = Frame(root)
        self.frame_middle = Frame(root)
        self.frame_bottom = Frame(root)

        # position the frames one above the other
        self.header_frame.pack(side=TOP)
        self.frame_middle.pack()
        self.frame_bottom.pack(side=BOTTOM)

        # initialize video url input
        # initialize video url input
        self.base_input = EntryWithPlaceholder(self.header_frame,
                                               placeholder="Link to a video from YouTube",
                                               width=90)

        self.confirm_button = Button(self.header_frame, text="Enter", command=self.confirm)
        self.download_button = Button(self.header_frame, text="Download", command=self.download)
        self.text_output = ScrolledText(self.frame_bottom, bg="black", width=85, height=20, fg="lightgrey")

        # position other elements
        self.base_input.pack(side=LEFT)
        self.confirm_button.pack(side=LEFT)
        self.download_button.pack(side=LEFT)
        self.text_output.pack(side=BOTTOM)

        self.log("Welcome \n Enter a link to a YouTube video and press \"Enter\" \n")

    def log(self, text):
        """ output "text" in the text field "label" """

        # Ты можешь каждый раз не передовать input элемент. Он у тебя всё равно один, просто используй self.text_output
        self.text_output.config(state=NORMAL)
        for row in text.split("\n"):
            current_time = "[{0}]: ".format(datetime.now().strftime("%H:%M:%S"))
            self.text_output.insert(END, f"{current_time} {row.strip()}\n")

        self.text_output.config(state=DISABLED)

    def download(self):
        """ A method that takes a number and starts downloading """

        try:
            video_number = int(self.base_input.get())
        except ValueError:
            self.log("The entered value must be a number")
            return

        if video_number > len(self.founded_videos) or video_number <= 0:
            self.log("Please input valid video number")

        self.log("Download starts...")

        # creates a folder "Downloads" in the current directory
        # Нахуй тебе makedirs, если ты создаешь всего 1 папку без вложенностей? Используй mkdir.

        if not os.path.exists(self.DOWNLOAD_DIR):
            os.mkdir(self.DOWNLOAD_DIR)

        self.founded_videos[video_number - 1].download(self.DOWNLOAD_DIR)
        self.log("Success!")

    def confirm(self):
        """ Seaching for a video and gives options for downloading """
        try:
            video_url = self.base_input.get()
            self.founded_videos = YouTube(video_url).streams.filter(progressive=True).all()

            if not self.founded_videos:
                self.log("Sorry, videos not found.")
                return

            self.log("{} videos found, select ...".format(len(self.founded_videos)))
            for index, video in enumerate(self.founded_videos, 1):
                name = video.default_filename
                size = bytes_to_human_readable(video.filesize)
                self.log(f"\t{index}. {name} {size}")

            self.log("\n Enter the number of the desired video in the field and click \"Download\" (default 1)")
            self.base_input.delete(0, last=END)

        except RegexMatchError:
            self.log("ERROR: The entered URL is incorrect")


if __name__ == "__main__":
    root = Tk()
    root.resizable(width=False, height=False)
    pt = GUI(root)
    root.mainloop()
