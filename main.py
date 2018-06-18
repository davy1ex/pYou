from tkinter import *
import pytube
from datetime import datetime
import os


class GUI:
	def __init__(self, master):
		master.title("pYou")

		# frames
		self.frame_top = Frame(master)
		self.frame_middle = Frame(master)
		self.frame_bottom = Frame(master)

		# link field
		self.href = Entry(self.frame_top, width=90)
		self.href.insert(END, "Link to a video from YouTube")

		# btn enter
		self.b_choice = Button(self.frame_top, text="Enter", command=self.choice)

		# btn download
		self.b_download = Button(self.frame_top, text="Download", command=self.download)

		# label (log)
		self.txt = Text(self.frame_bottom, bg="black", width=85, height=20, fg="lightgrey")

		# started log
		self.log(self.txt, "Welcome")
		self.log(self.txt, "Enter a link to a YouTube video and press \"Enter\"")
		self.log(self.txt, "")

		# packing frames
		self.frame_top.pack(side=TOP)
		self.frame_middle.pack()
		self.frame_bottom.pack(side=BOTTOM)

		# packing widgets
		self.href.pack(side=LEFT)
		self.b_choice.pack(side=LEFT)
		self.b_download.pack(side=LEFT)
		self.txt.pack(side=BOTTOM)

	def log(self, label, text):
		""" output "text" in the text field "label" """
		# allows write
		label.config(state=NORMAL)
		label.insert(END, "[{0}]: ".format(datetime.now().strftime("%H:%M:%S")) + text + '\n')

		# prohibits writing
		label.config(state=DISABLED)
		label.see("end")

	def download(self):
		""" A method that takes a number and starts downloading """
		self.choiced = self.href.get()
		self.log(self.txt, "Start downloading...")
		# creates a folder "Downloads" in the current directory
		try:
			os.makedirs(os.getcwd() + "/Downloads")
		except:
			pass
		try:
			path = os.getcwd() + "/Downloads"
			self.yt[int(self.choiced) - 1].download(path)
			self.log(self.txt, "Finished")
		except:
			self.log(self.txt, "ERROR")
		self.log(self.txt, "")

	def choice(self):
		""" Seaching for a video and gives options for downloading """
		try:
			self.yt = pytube.YouTube(self.href.get())
			self.log(self.txt, "Found:")
			self.log(self.txt, "")
			self.yt = self.yt.streams.filter(progressive=True).all()
			for i in self.yt:
				# name.format size
				self.log(self.txt, "{0} {1} mb".format(i.default_filename, str(i.filesize / 1024 / 1024)[:3]))
			self.log(self.txt, "")
			self.log(self.txt, "Enter the number of the desired video in the field and click \"Download\" (default 1)")
			self.log(self.txt, "")
			self.href.delete(0, last=END)
			self.href.insert(END, "1")
		except:
			self.log(self.txt, "ERROR")
			self.log(self.txt, "")


if __name__ == "__main__":
	root = Tk()
	root.resizable(width=False, height=False)
	pt = GUI(root)
	root.mainloop()