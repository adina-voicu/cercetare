#! /usr/bin/python

import csv
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import pymongo
from collections import defaultdict
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

wnl = WordNetLemmatizer()

def pos(tag):
    if tag.startswith('JJ'):
        return 'a'
    elif tag.startswith('VB'):
        return 'v'
    elif tag.startswith('NN'):
        return 'n'
    elif tag.startswith('RB'):
        return 'r'
    else:
        return ''
def lemma(sentences):
	z = []
	for sentence in sentences:
		x = [(wnl.lemmatize(word, pos(tag)), pos(tag)) for word, tag in pos_tag(word_tokenize(sentence)) if pos(tag) in ['n', 'v', 'a', 'r']]
		z = z + x
	return z

def filter(prop):
	filttags = []
	for sent in prop:
		grammar = "NP:{<a>* <n>*}"
		cp = nltk.RegexpParser(grammar)
		result = cp.parse(sent) 
		filttags.append(result) # create a tree with chunks with pos like grammar and the rest of words
	return filttags

def terms(sentences):
	y = []
	for sent in sentences:
		for subtree3 in sent.subtrees():
			if subtree3.label() == 'NP':
				strp = ' '.join([w.rsplit('/', 1)[0] for w in str(subtree3).split()])
				strip = ' '.join([w.split('(NP', 1)[0] for w in strp.split()])
				y.append(strip)
	return y

def clean(str):
    str = ''.join([c for c in str if c in 'ABCDEFGHIJKLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890- \''])
    return str
def clean_sentence(s):
    for word in s:
        lst_cleaned = []
        for items in s:
            lst_cleaned.append(clean(items))
        return lst_cleaned

def insert(docs):
    con = pymongo.MongoClient()
    coll = con.test.doc
    for doc in docs:
        coll.save(doc)

def stop(txt):
    stopwords = nltk.corpus.stopwords.words('english')
    x=[]
    for w in txt.split():
        if w not in stopwords:
            x.append(w)
        else:
            continue
    return ' '.join(x)
		
with open('dtcfs.csv') as csvf:
    reader = csv.DictReader(csvf, delimiter='	')
    header = ['id', 'conf', 'title', 'author', 'year', 'abstract', 'conf_short', 'theme']
    output = []
    for line in reader:
        row = {}
        for field in header:
            if field == 'abstract':
                row['abstract'] = stop(' '.join(clean_sentence(terms(filter([lemma(nltk.sent_tokenize(line['abstract'].lower()))])))))
            else:
                row[field] = line[field]
        output.append(row)
	insert(output)
print output
