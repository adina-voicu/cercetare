import nltk
from nltk import word_tokenize
import math
import pymongo
from collections import Counter
from pymongo import MongoClient
from random import randint
from gensim import corpora, models, similarities
from operator import itemgetter

resp = raw_input('Select method: \n 1 - Okapi \n 2 - C-value \n 3 - C-value okapi \n 4 - C-value tf-idf \n R: --> ')
if resp not in ["1","2","3","4"]:
	resp = raw_input("Try again! \n Select method (1, 2, 3 or 4): \n 1 - Okapi \n 2 - C-value \n 3 - C-value okapi \n 4 - C-value tf-idf \n R: --> ")

def stop(txt):
    stopwords = nltk.corpus.stopwords.words('english')
    x=[]
    for w in txt.split():
        if w not in stopwords:
            x.append(w)
        else:
            continue
    return ' '.join(x)

con = pymongo.MongoClient()
collection = con.test.doc
docs = list(collection.find())

#terms = [] # list of documents with lemmatized words
documents = [] # list with initial documents
dictngrams = {}
dtfreq = {}
countdoc = {}
corpus_length = 0
for doc in docs:
	documents.append([doc['abstract']])
	corpus_length += len(doc['abstract'].split())
#	terms.append([doc['terms']])
	grm = doc['ngrams']
	dct = {}
	for ngrm in grm:
		ngram = stop(ngrm)
		dct[ngram] = grm[ngrm]
		if ngram not in countdoc.keys():						   
			dtfreq[ngram] = grm[ngrm]
			countdoc[ngram] = 1 
		else:
			dtfreq[ngram] += grm[ngrm]
			countdoc[ngram] = countdoc[ngram] + 1
	dictngrams[doc['id']] = dct
lencorpus = len(docs) #number of documents in corpus
print corpus_length

print "count documnts:", countdoc["database"]
ngramdict = {}
ngrams = [] # list of documents with candidate terms (filtered)
for doc in dictngrams:
	n = []
	for ngram in dictngrams[doc]:
		docnb = countdoc[ngram]
		idf = math.log((float(lencorpus)/countdoc[ngram]), 10)
		tup = (ngram, dictngrams[doc][ngram], idf, doc)
		dictngrams[doc][ngram] = tup
		n.append(tup)
	ngrams.append(n)
print 'lists created', lencorpus

def get_substring(str):
	lns = len(str.split())
	x = [' '.join(str.split()[i:j+1]) for i in xrange(lns) for j in xrange(i,lns) if lns > len(str.split()[i:j+1])]
	return x

avgdl = float(corpus_length)/len(documents)
k = 1.2
b = 0.75
maxlen = 0 # max length of candidate strings
fs = open('Okapi500.txt', 'w')
dctokapi = {}
dcttfidf = {}
for i in dictngrams:
	D = 0
	D = len(documents[int(i)-1][0].split())
	for j in dictngrams[i]:
		ngram =  dictngrams[i][j][0]
		idf =  math.log((float(lencorpus)/countdoc[ngram]), 10)
		nrdoc = int( dictngrams[i][j][3])
		f =  dictngrams[i][j][1]
		score = idf * ((f * (k + 1))/(f + k * (1 - b + b * (D/avgdl))))
		tfidf = f * idf
		if maxlen < len(ngram.split()):
			maxlen = len(ngram.split())
		if ngram not in dctokapi:
			dctokapi[ngram] = score
			dcttfidf[ngram] = tfidf
		else:
			dcttfidf[ngram] += tfidf
			dctokapi[ngram] += score
		dictngrams[i][j] = (ngram, f, idf, D, score, tfidf, int(nrdoc))

if resp == "1":
	fs = open('Okapi500.txt', 'w')
	for i in sorted( ((v,k) for k,v in dctokapi.iteritems()), reverse=True):
		#print i[1], i[0]
		s = ' '.join([i[1], ' :', str(i[0]), "\n"])
		fs.write(s)
	fs.close()
	print "File Okapi created!"

elif resp == "2": #create dict with sum of term frequency for c-value
	method = "C-value"
	dcttst = dtfreq

elif resp == "3": #create dict with okapi score for c-value
	method = "C-value_Okapi"
	fs = open('okapi.txt', 'w')
	dcttst = dctokapi
	for i in sorted( ((v,k) for k,v in dcttst.iteritems()), reverse=True):
		s = ' '.join([i[1], ' :', str(i[0]), "\n"])
		fs.write(s)
	fs.close()
	print "File Okapi.txt created!"

elif resp == "4":
	method = "C-value_TF-IDF"
	fs = open('tfidf.txt', 'w')
	dcttst = dcttfidf
	for i in sorted( ((v,k) for k,v in dcttst.iteritems()), reverse=True):
		s = ' '.join([i[1], ' :', str(i[0]), "\n"])
		fs.write(s)
	fs.close()
	print 'File tfidf created!'
corpus = []
for i in dictngrams:
	for j in dictngrams[i]:
		corpus.append(dictngrams[i][j])
	
if resp != "1":
	substr = {}
	threshold = 1
	dcval = {} # create dict - {word:cvalue}
	for ngram in dcttst:
		if len(ngram.split()) == maxlen:
			a =  ngram
			l = len(a.split())
			fa = dcttst[a] 
			Cvalue = math.log(l+1, 2) * fa
			if Cvalue >= threshold: 
				if a not in dcval.keys():
					dcval[a] = Cvalue
				substrings = get_substring(a)
				for b in substrings:
					if b in dcttst.keys():
						if b not in substr.keys():
							cb = 1            # number of longer candidates
							fb = dcttst[b] # total frequency of b in the corpus
							tb = dcttst[a] # frequency of a
						else:
							tb = substr[b][1] + dcttst[a] # frequency of a
							cb = substr[b][2] + 1
							fb = substr[b][0]
						substr[b] = [fb, tb, cb]
	for l in range(maxlen-1, 0, -1):
		for a in dcttst:
			if len(a.split()) == l:
				fa = dcttst[a]
				if a not in substr.keys():
					Cvalue = math.log(l+1, 2) * fa
				else:
					fa = substr[a][0]
					ta = substr[a][1]
					ca = substr[a][2]
					Cvalue = float(math.log(l+1, 2)) * (fa - 1/ca * ta)
				if Cvalue >= threshold:
					dcval[a] = Cvalue
					substrings = get_substring(a)
					for b in substrings:
						if b in dcttst.keys():
							if b not in substr.keys():
								cb = 1            # number of longer candidates
								fb = dcttst[b] # total frequency of b in the corpus
								tb = dcttst[a] # frequency of a
							else:
								tb = substr[b][1] + dcttst[a] # frequency of b
								cb = substr[b][2] + 1
								fb = substr[b][0]
							substr[b] = [fb, tb, cb]
	fcval = open("%s.txt" %(method,), 'w')
	for i in sorted( ((v,k) for k,v in dcval.iteritems()), reverse=True):
		s = ' '.join([i[1], ' :', str(i[0]), "\n"])
		fcval.write(s)
	print 'File %s created!' %(method,)
