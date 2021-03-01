#this script performs a topic modeling algorithm on a given 

import spacy
spacy.load("en")
from spacy.lang.en import English
import nltk
nltk.download("wordnet")
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download("stopwords")
import gensim
from gensim import corpora
import pickle
import pyLDAvis.gensim

#turn each word in the text into a parseable "token"

parser = English()

def Tclean(text):
	text = text.replace("\\","").replace("/"," ").replace(","," ")
	return text

def tokenize(text):
	lda_tokens = []
	tokens = parser(text)
	for token in tokens:
		if token.orth_.isspace():
			continue
		elif token.like_url:
			lda_tokens.append("URL")
		elif token.orth_.startswith("@"):
			lda_tokens.append("SCREEN_NAME")
		else:
			lda_tokens.append(token.lower_)
	return lda_tokens

#convert each word to its root word to correctly flag each instance where it occurs

def get_lemma(word):
	lemma = wn.morphy(word)
	if lemma is None:
		return word
	else:
		return lemma

#filter stop words

en_stop = ["your","dont","ourselves", "between", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "an", "be", "some", "for", "do", "its", "it's", "such", "into", "of", "most", "itself", "off", "is", "am", "or", "who", "whom", "as", "from", "each", "the", "themselves", "until", "below", "are", "we", "these", "through", "don't", "nor", "were", "more", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "all", "no", "when", "at", "any", "them", "same", "and", "been", "have", "in", "will", "on", "does", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "has", "just", "where", "too", "only", "which", "those", "after", "few", "whom", "being", "if", "theirs", "against", "a", "by", "it", "how", "was", "here", "than","theres","much","back","never","ever","make","come","comes","makes","go","goes","went","around","like"]

#put it all together

def prepare_text_for_lda(text):
	Ctext = Tclean(text)
	Cltext = Tclean(Ctext)
	#print(Cltext)
	tokens = tokenize(Cltext)
	tokens = [token for token in tokens if token not in en_stop]
	tokens = [token for token in tokens if len(token) > 3]
	token = [get_lemma(token) for token in tokens]
	#print(tokens)
	return tokens

#open and convert our sample text

text_data = []

with open("clean.csv") as f:
	for line in f:
		tokens = prepare_text_for_lda(line)
		text_data.append(tokens)

#perform LDA

dictionary = corpora.Dictionary(text_data)
corpus=[dictionary.doc2bow(text) for text in text_data]
pickle.dump(corpus, open("corpus.pkl","wb"))
dictionary.save("dictionary.gensim")

NUM_TOPICS = 10

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model10.gensim')

topics = ldamodel.print_topics(num_words=10)
for topic in topics:
	print(topic)

#visualize it
'''
dictionary = gensim.corpora.Dictionary.load("dictionary.gensim")
corpus = pickle.load(open("corpus.pkl","rb"))
lda = gensim.models.ldamodel.LdaModel.load("model10.gensim")

lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics = False)
pyLDAvis.display(lda_display)
'''