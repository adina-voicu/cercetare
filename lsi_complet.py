# de pe pagina 1 https://radimrehurek.com/gensim/tut1.html

from gensim import corpora, models, similarities
import pymongo
from pymongo import MongoClient
from random import randint

con = pymongo.MongoClient()
collection = con.test.docs
#docs = [{"_id" : 2, "foo" : "HELLO"}, {"_id" : 2, "Blah" : "Bloh"}]
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
#documents = ["Human machine interface for lab abc computer applications", "A survey of user opinion of computer system response time", "The EPS user interface management system", "System and human system engineering testing of EPS", "Relation of user perceived response time to error measurement", "The generation of random binary unordered trees", "The intersection graph of paths in trees", "Graph minors IV Widths of trees and well quasi ordering", "Graph minors A survey"]

# vectorizarea documentelor, o lista de liste cu termeni:
# aceast lista trebuie sa contina doar lemme. 
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

# Utilizarea modelului LSI
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)


#for topic in lsi.print_topics():
#    print topic

# pentru a vedea probabilitatea cu care apartine un documnet la un topic
corpus_lsi = lsi[corpus_tfidf]
top = []
for l in corpus_lsi:
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
