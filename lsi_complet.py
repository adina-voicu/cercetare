# de pe pagina 1 https://radimrehurek.com/gensim/tut1.html

from gensim import corpora, models, similarities
import pymongo
from pymongo import MongoClient

con = pymongo.MongoClient()
collection = con.test.docs
docs = list(collection.find())
#print docs
documents = []
for doc in docs:
    text = doc['abstract']
    documents.append(text)
print(documents)

# vectorizarea documentelor, lista de liste cu termeni:
texts = [[word for word in document.lower().split()] for document in documents]
#print texts
#dictionar id 2 word
dictionary = corpora.Dictionary(texts)
for key in dictionary:
    print key, dictionary[key]

# lista de liste cu termeni si frecventa (co-occurrence) 
# in literatura bag-of-words integer counts
corpus = [dictionary.doc2bow(text) for text in texts]
print corpus

# initializarea modelului TF*IDF
tfidf = models.TfidfModel(corpus)

# vectorizare TF*IDF - matrice
corpus_tfidf = tfidf[corpus]

for doc in corpus_tfidf:
    print doc

# Utilizarea modelului LSI
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)

for topic in lsi.print_topics():
    print topic

# pentru a vedea probabilitatea cu care apartine un documnet la un topic
corpus_lsi = lsi[corpus_tfidf]

for doc in corpus_lsi:
    print doc
