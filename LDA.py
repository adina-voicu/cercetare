import numpy as np
from gensim import corpora, models, similarities
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
themes = []
for doc in docs:
    text = doc['theme']
    themes.append(text)

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
corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
#    print doc

# generate LDA model
lda = models.ldamodel.LdaModel(corpus_tfidf, num_topics=5, id2word = dictionary, passes=350)

print (lda.print_topics(num_topics=5, num_words=10))


# pentru a vedea probabilitatea cu care apartine un documnet la un topic
corpus_lda = lda[corpus_tfidf]
top = []
for l in corpus_lda:
#    print l
    if not l:
        topic = randint(0,4)
    else:
        maximum = l[0][1]
    for elem in l:
        if maximum< elem[1]:
            maximum = elem[1]
            topic = elem[0]
    top.append(topic)
print top
print themes
thtop = zip(themes,top)
print z

clase = {
    'medical' : {0:0, 1:0, 2:0, 3:0, 4:0},
    'database' : {0:0, 1:0, 2:0, 3:0, 4:0},
    'theory' : {0:0, 1:0, 2:0, 3:0, 4:0},
    'datamining' : {0:0, 1:0, 2:0, 3:0, 4:0},
    'visu' : {0:0, 1:0, 2:0, 3:0, 4:0}
}
for i in thtop:
    clase[i[0]][i[1]] +=1
print clase
