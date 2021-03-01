from spellchecker import SpellChecker
import csv
import re

#find all unknown words

spell = SpellChecker(language=u"en",distance=5)
spell_spa = SpellChecker(language=u"es",distance=5)
spell_fra = SpellChecker(language=u"fr",distance=5)
spell_ger = SpellChecker(language=u"de",distance=5)

forbidden_words = ["christopher","poindexter","nikita","gill","rupi","kaur","rupikaur_","tyler","knott","gregson","ladybookmad","r.","h.","r.h.sin","atticus","atticuspoetry","keyballah","marie","jo","cleo","wade","austin","kleon","austinkleon","langleav","amazon","sin","amanda","lovelace","lady","schwarz","com","shipping","twitter","ladybirds","bestselling","york","author","instagram"]

beforeText = []
afterText = []

with open("results.csv","r") as f:
	for line in f:
		beforeText.append(str(line))

for poem in beforeText:
	poemList = poem.split(",")
	for word in poemList:
		if word == "":
			poemList.remove(word)
		if word == ",":
			poemList.remove(word)
	for word in poemList:
		if word.casefold() in forbidden_words:
			poemList.remove(word)
			continue
		if len(word) == 1:
			if word.casefold() != "i" and word.casefold() != "a" and word != "/":
				poemList.remove(word)
				continue
		if len(word) > 1 and word == len(word) * word[0]:
			poemList.remove(word)
			continue
		for char in word:
			if char.isdigit():
				try:
					poemList.remove(word)
				except:
					continue
			if char.isalpha() == False:
				if char != "'" and char != "/":
					try:
						poemList.remove(word)
					except:
						continue
	for word in poemList:
		word = word.casefold()
		if word == "":
			poemList.remove(word)
		if word == ",":
			poemList.remove(word)
	misspelled = spell.unknown(poemList)
	misspelled_eng = len(misspelled)
	misspelled_spa = len(spell_spa.unknown(poemList))
	misspelled_fra = len(spell_fra.unknown(poemList))
	misspelled_ger = len(spell_ger.unknown(poemList))
	if misspelled_eng > misspelled_spa or misspelled_eng > misspelled_fra or misspelled_eng > misspelled_ger or misspelled_eng > len(poemList) * .5:
		continue
	completePoem = " ".join(poemList).strip()
	poemList = completePoem.split()
	poemList = [word.casefold() for word in poemList]
	afterText.append(poemList)

for poem in afterText:
	if len(poem) < 4:
		afterText.remove(poem)
		continue
	if len(re.findall("/", str(poem))) > len(poem) * .5:
		afterText.remove(poem)
		continue
	linenos = [i for i, x in enumerate(poem) if x == "/"]
	for numb in linenos:
		for othernumb in linenos:
			if numb == othernumb:
				continue
			elif abs(numb-othernumb) > 1:
				continue
			else:
				try:
					del poem[numb]
				except:
					continue
			linenos = [i for i, x in enumerate(poem) if x == "/"]
	if poem[-1] == "/":
		del poem[-1]

outputF = open("clean.csv","a",newline="")
writer = csv.writer(outputF)

for poem in afterText:
	writer.writerow(poem)
outputF.close()