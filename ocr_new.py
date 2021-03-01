try:
	from PIL import Image, ImageEnhance, ImageFilter
except ImportError:
	import Image, ImageEnhance, ImageFilter
import pytesseract
#from spellchecker import SpellChecker
import re
from deskew import determine_skew
from skimage import io
from skimage.transform import rotate
from skimage.color import rgb2gray
from skimage.exposure import adjust_sigmoid
import numpy as np
#import wordninja
import os
import csv
from string import ascii_letters, digits
from textblob import Word
from textblob import TextBlob


def enhance_image(path):
	#try to read the image, alert if it's not readable
	try:
		image = io.imread(path)
	except:
		print("could not read target image")
		return False
	#make grayscale
	grayscale = rgb2gray(image)
	#increase contrast
	contrasted = adjust_sigmoid(grayscale, cutoff=0.5, gain=10, inv=False)
	#render text horizontal
	angle = determine_skew(contrasted)
	if abs(angle) > 75:
		angle2 = (abs(angle) - 90) * (angle / abs(angle))
	else:
		angle2 = angle
	rotated = rotate(contrasted, angle2, resize=True) * 255
	#save as 'output.png'
	io.imsave("output.png", rotated.astype(np.uint8))

def get_text(path):
	#try to extract text from 'output.png'
	try:
		text = pytesseract.image_to_string(path,lang="eng",config='--psm 6')
		return text
	except:
		print("could not extract text from image")
		return False

def clean_text(text):
	#replace special characters except apostrophes
	try:
		pass1 = text.replace("\n"," \ ")
	except:
		return False
	pass2 = "".join([ch for ch in pass1 if ch in (ascii_letters + "'" + " "+" \ ")])
	pass3 = pass2.replace("\\"," / ")
	pass4 = pass3.split()
	#make lowercase
	pass5 = [word.casefold() for word in pass4]
	#try to omit non-english poems
	passString = " ".join(pass5)
	passBlob = TextBlob(passString)
	try:
		if passBlob.detect_language() != "en":
			print("not english")
			return False
	except:
		return False
	#spellcheck
	pass6 = []
	for i in range(0,len(pass5)):
		word = pass5[i]
		try:
			nextword = pass5[i+1]
		except:
			nextword = ""
		#omit single-character tidbits (which are usually wrong)
		if len(word) == 0 and word != "a" and word != "i":
			continue
		#omit repeated words (which are usually wrong)
		if word == nextword:
			continue
		#get list of possible spellings
		word2 = Word(word)
		wordlist = word2.spellcheck()
		bestguess = wordlist[0]
		#if a possible spelling seems fairly likely, go with it; otherwise, skip the word
		if bestguess[1] > .7:
			pass6.append(bestguess[0])
	#omit repeated characters and beginning/ending linebreaks
	pass7 = []
	for i in range(0,len(pass6)):
		word = pass6[i]
		try:
			nextword = pass6[i+1]
		except:
			nextword = ""
		if word == nextword:
			continue
		if word == "/" and (nextword == "" or i == 0):
			continue
		pass7.append(word)
	#if the poem is too short - because all the words were misspelled - skip it
	if len(pass7) < 6:
		return False
	return pass7

targets = os.listdir("sample")
fl = open("results.csv","a",newline="")
writer = csv.writer(fl)

for target in targets:
	#print(target)
	try:
		enhance_image("sample/%s" % target)
	except:
		print("could not find image")
		continue
	text = get_text("output.png")
	cleaned = clean_text(text)
	print(cleaned)
	if cleaned != False:
		writer.writerow(cleaned)