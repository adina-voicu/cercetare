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
ngrams = []
dictngrams = {}
for doc in docs:
	abstract = doc['abstract']
	documents.append(abstract)
	text = doc['terms']
	terms.append(text)
	grm = doc['ngrams']
	for ngram in grm:
		ngrams.append([ngram])
		dictngrams[ngram] = grm[ngram]
#print dictngrams
#print ngrams
#print terms

maxlength = 0
for ngram in ngrams:
	wordslist = [word for word in ' '.join(ngram).split()]
	if maxlength < len(wordslist):
		maxlength = len(wordslist)
#print maxlength

sorted_dict = {}
listngrams = []
#for str in dictngrams:
#	if len(str.split()) == maxlength:
#		listngrams.append([str, dictngrams[str]])
#print listngrams
for i in range(maxlength, 1, -1):
	for string in dictngrams:
		varlst = []
		if len(string.split()) == i:
			lsti = []
			PTa = 0
			Sfb = 0
			for ngram in ngrams:
				if any(string in text for text in ngram if string != text):
					PTa += 1 # nr of longer terms - P(T(a))
					Sfb += dictngrams[' '.join(ngram)] # Sum f(b), b in T(a)
					lsti.extend([' '.join(ngram)]) # list of longer terms - T(a)
			varlst.extend([string, dictngrams[string], PTa, Sfb, lsti]) #len(string), frecventa totala, fq in termeni mai lungi, lista termenilor
			listngrams.append(varlst)
#print listngrams
f = open('cvalfile.txt', 'w')
def get_substrings(input_string):
	length = len(input_string.split())
	return [' '.join(input_string.split()[i:j+1]) for i in xrange(length) for j in xrange(i,length) if length > len(input_string.split()[i:j+1]) > 1]
#print get_substrings('declarative rule based style')
threshold = 1.5
candterms = []
substr = {}
for ngrams in listngrams:
	if len(ngrams[0].split()) == maxlength:
#		print ngrams[0]
		a = (1 + float(len(ngrams[0].split())))
		fa = float(ngrams[1])
		cvalue = math.log(a, 2) * fa
		print ngrams[0], cvalue
		if cvalue >= threshold:
			candterms.append(ngrams[0])
			for b in get_substrings(ngrams[0]):
				if b in substr.keys():
					tb = substr[b][1] + dictngrams[ngrams[0]]
					cb = substr[b][2] + 1
				else:
					cb = 1
					fb = 0
					tb = dictngrams[ngrams[0]]
					for s in terms: 
						if b in s:
							fb += 1
				substr[b] = [fb, tb, cb]
#				print b, fb

for ngrams in listngrams:
	if len(ngrams[0].split()) < maxlength:
		if ngrams[0] not in substr.keys():
			a = (1 + float(len(ngrams[0].split())))
			fa = float(ngrams[1])
			cvalue = math.log(a, 2) * fa
			print ngrams[0], cvalue
		else:
			a = (1 + float(len(ngrams[0].split())))
			fa = float(ngrams[1])
			ca = float(substr[ngrams[0]][2])
			ta = float(substr[ngrams[0]][1])
			cvalue = math.log(a, 2) * (fa - 1/ca * ta)
			print ngrams[0], cvalue
			if cvalue >= threshold:
				candterms.append(ngrams[0])
				for b in get_substrings(ngrams[0]):
					if b in substr.keys():
						tb = substr[b][1] + dictngrams[ngrams[0]]
						cb = substr[b][2] + 1
					else:
						cb = 1
						fb = 0
						tb = dictngrams[ngrams[0]]
						for s in terms: 
							if b in s:
								fb += 1
					substr[b] = [fb, tb, cb]

#	for ngram in ngrams:
#		print ngram
print candterms
