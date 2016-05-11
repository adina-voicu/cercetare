import numpy as np
from gensim import corpora, models, similarities
import gensim
import lda
import lda.datasets
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
#print(documents)

# vectorizarea documentelor, o lista de liste cu termeni:
texts = [[word for word in document.lower().split()] for document in documents]
#print texts
#dictionar id 2 word
dictionary = corpora.Dictionary(texts)
#for key in dictionary:
#    print key, dictionary[key]

# lista de liste cu termeni si frecventa (co-occurrence) 
# in literatura bag-of-words integer counts
corpus = [dictionary.doc2bow(text) for text in texts]
#print corpus

# initializarea modelului TF*IDF
tfidf = models.TfidfModel(corpus)

# vectorizare TF*IDF
# Aceasta este matricea despre care iti ziceam in mail
corpus_tfidf = tfidf[corpus]


# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=5, id2word = dictionary, passes=20)
print(ldamodel.print_topics(num_topics=5, num_words=10))


