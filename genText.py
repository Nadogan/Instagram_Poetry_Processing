#this script generates 20 instapoems based on a sample
#run from command line, and specify the path of the sample in the command
#the sample has to be a csv file

import numpy as np
import random
import statistics

#gets averages from the sample poems so that our poems are statistically consistent with the sample
def get_stats(path):
	text = []
	textlengths = []
	linelengths = []
	with open(path) as f:
		for line in f:
			text.append(line)
	for poem in text:
		poemList = poem.split(",")
		poemList = [item for item in poemList if item != "" and item != "\n"]
		lineIndices = [i for i, x in enumerate(poemList) if x == "/"]
		textlengths.append(len(poemList) - len(lineIndices))
		for i in range(len(lineIndices) - 1):
			leN = lineIndices[i]
			if i ==0:
				linelengths.append(leN)
			else:
				linelengths.append(leN - lineIndices[i-1])
	nopoems = len(text)
	poemLen = int(round(statistics.median(textlengths)))
	lineLen = int(round(sum(linelengths) / len(linelengths)))
	return nopoems, poemLen, lineLen

#gets separate poems from the sample csv file
def extract_text(path):
	text = []
	with open(path) as f:
		for line in f:
			text.append(line)
			text.append(",")
	strtext = " ".join([str(elem) for elem in text])
	cleantext = strtext.replace("\\","").replace("/"," ").replace(","," ").replace("(","").replace(")","").replace("@","").replace("'","").replace("!","").replace("#","").replace("$","").replace("%","").replace("^","").replace("&","").replace("*","").replace("[","").replace("]","").replace("'","").replace('"',"")
	cleantext = " ".join(cleantext.split())
	cleantext = cleantext.split()
	for item in cleantext:
		if item.isdigit() == True:
			cleantext.remove(item)
		else:
			continue
	cleantext = " ".join(cleantext)
	cleantext = cleantext.casefold()
	return cleantext

#identifies all word pairs in the extracted poems
def make_pairs(corpus):
	for i in range(len(corpus)-1):
		yield (corpus[i], corpus[i+1])

#generates a corpus of words from the word pairs
def make_corpus(text):
	corpus = text.split()
	return corpus

#creates a dictionary of each word in the sample, and all the words that follow it
def make_dict(corpus):
	pairs = make_pairs(corpus)
	word_dict = {}
	for word_1, word_2 in pairs:
		if word_1 in word_dict.keys():
			word_dict[word_1].append(word_2)
		else:
			word_dict[word_1] = [word_2]
	return word_dict

#with an output poem, divides it into lines based on the statistical averages from the sample
def addlines(text,lineLen):
	textList = text.split()
	noLines = int(round(len(textList) / lineLen))
	lineBreaks = []
	for i in range(noLines):
		x = random.randrange(int(round(lineLen//2)), int(round(lineLen*1.5)))
		if i == 0:
			lineBreaks.append(x)
		else:
			lineBreaks.append(x + lineBreaks[i-1])
	for beak in lineBreaks:
		try:
			textList.insert(beak,"/")
		except:
			continue
	output = " ".join(textList)
	if output[-1] == "/":
		output = output[:-1]
	return output

#create a poem from the sample
def generate_poem(numb, path):
	text = extract_text(path)
	corp = make_corpus(text)
	dicp = make_dict(corp)
	nopoems, avglen, avgLine = get_stats(path)
	print("Number of poems: %d" % nopoems)
	print("Average word length of poems: %d" % avglen)
	print("Average length of each poem line: %d" % avgLine)
	for i in range(numb):
		first_word = makefirstword(corp)
		chain = [first_word]
		leng = random.randrange(int(round(avglen//4)),int(round(avglen*3)))
		for i in range(leng):
			chain.append(np.random.choice(dicp[chain[-1]]))
		output = " ".join(chain)
		output = clean(output)
		output = addlines(output,avgLine)
		print("Poem:")
		print(output)

#eliminate certain unhelpful or generic words from the sample
def clean(string):
	forbidden_words = ["christopher","poindexter","nikita","gill","rupi","kaur","rupikaur_","tyler","knott","gregson","ladybookmad","r.","h.","r.h.sin","atticus","atticuspoetry","keyballah","marie","jo","cleo","wade","austin","kleon","austinkleon","langleav","amazon","sin","amanda","lovelace","lady","schwarz","com","shipping","twitter","ladybirds","bestselling","york","author"]
	textList = string.split(" ")
	for word in textList:
		if word.casefold() in forbidden_words:
			textList.remove(word)
		for char in word:
			if char.isdigit():
				try:
					textList.remove(word)
				except:
					continue
	textNew = " ".join(textList)
	return textNew

#choose the first word to begin the markov chain
def makefirstword(corpus):
	forbidden_words = ["and","but","having","was","where","how","int","ae","en","or","ee","elle","pg","int","oa","ce","of","christopher","poindexter","nikita","gill","rupi","kaur","rupikaur_","tyler","knott","gregson","ladybookmad","r.","h.","r.h.sin","atticus","atticuspoetry","keyballah","marie","jo","cleo","wade","austin","kleon","austinkleon","langleav","amazon","sin","amanda","lovelace","lady","schwarz","com","shipping","twitter","ladybirds"]
	output = ""
	while True:
		output = np.random.choice(corpus)
		if output.casefold() not in forbidden_words:
			break
	return output

#generates the poems
generate_poem(20,"clean.csv")