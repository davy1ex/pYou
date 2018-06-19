import argparse
import os
import time

from pytube import YouTube
from pytube.exceptions import RegexMatchError


def createParser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--link")
	parser.add_argument("-f", "--format", nargs="?")
	parser.add_argument("-p", "--path", nargs="?")

	return parser


if __name__ == '__main__':
	parser = createParser()
	namespace = parser.parse_args()

	# if namespace.llnk:
	# 	try:
	# 		yt = YouTube(namespace.link)
	# 	except RegexMatchError:
	# 		print("ERROR: The intered URL is incorrect")
	# else:
	# 	raise "ERROR: link was not specified"
	try:
		yt = YouTube(namespace.link)
	except RegexMatchError:
		print("ERROR: The intered URL is incorrect")
		# return
	except TypeError:
		print("ERROR: The intered URL is incorrect")
		# return
	if namespace.format:
		if namespace.format == "mp3":
			yt = yt.streams.filter(only_audio=True).all()	
		else:
			yt = yt.streams.filter(file_extension=namespace.format).all()
	else:
		yt = yt.streams.filter(file_extension="mp4").all()

	name = yt[0].default_filename

	if namespace.path:
		path = os.path.join(os.getcwd(), namespace.path)
		# name = yt[0].default_filename
		#print(name, "will save here:", path)
	else:

		path = os.path.join(os.getcwd(), "Downloads")
		# print(name, "will save here:", path)
	
	print("Downloading...")
	start_time = time.time()
	try:
		os.makedirs(os.path.join(os.getcwd(), "Downloads"))
	except:		
		pass
	yt[0].download(path)
	
	if namespace.format == "mp3":
		#name = yt[0].default_filename
		print("Formating...")
		new_name = name.replace(name.split(".")[1], "mp3")
		try:
			os.rename(os.path.join(path, name), os.path.join(path, new_name))
		except FileExistsError:
			print("File already exists")
	# print("--- %s seconds ---" % (time.time() - start_time))
	time = time.time() - start_time
	print(time)
	print("Finished with", str(time.time() - start_time)[0:3], "Sec.")
