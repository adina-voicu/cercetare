import nltk
from nltk import word_tokenize
import math
import pymongo
from collections import Counter
from pymongo import MongoClient
from random import randint
from gensim import corpora, models, similarities
	
con = pymongo.MongoClient()
collection = con.test.doc
docs = list(collection.find())

terms = []
documents = []
for doc in docs:
	abstract = doc['abstract']
	documents.append(abstract)
	text = doc['terms']
	terms.append(text)

#calcul IDF
countword = {}
allwordinstances = []
 
for term in terms:
	words = [i for i in term.split()]
	allwordinstances += words
	countword = dict(Counter(allwordinstances)) #Creates a dictionary of the number of times the word is iterated through the entire corpus
#print countword
newvalues = {}
# formula IDF
for key, value in countword.iteritems():
	newvalues[key] = math.log((float(len(documents)) - float(value) + 0.5)/(float(value) + 0.5))

texts = [[word for word in document.split()] for document in terms] # lista cu documentele preprocesate
docs = [[word for word in document.split()] for document in documents] # lista cu documentele initiale
count = 0
# calcul avgdl
for i in range(0,len(docs)):
	count += len(docs[i])
	print count
avgdl = float(count)/len(docs)
print avgdl

#dictionar id 2 word
dictionary = corpora.Dictionary(texts)

# lista de liste cu termeni si frecventa (co-occurrence) 
# in literatura bag-of-words integer counts
corpus = [dictionary.doc2bow(text) for text in texts]
# creare dictionar cu documentele si cuvintele (id: word)
c = 0
x = {}
for sent in corpus:
	c = c + 1
	x[c] = dict(sent)
k1 = 1.5
b = 0.75
for i in x:
	score = 0
	okapi = 0
	for key, val in x[i].iteritems(): # key = word id
		lst = []
		lst.extend([dictionary[key], newvalues[dictionary[key]], val, len(docs[i-1]), avgdl]) # word [0], IDF [1], aparitii t in D [2], |D| [3], avgdl [4]
		x[i][key] = lst
		score = x[i][key][1] * (x[i][key][2] * (k1 + 1))/ (x[i][key][2] + k1 *(1 - b + b * x[i][key][3]/x[i][key][4]))
		okapi += score
		lst.append(score)
		x[i][key] = lst
		print x[i][key]
	print okapi
