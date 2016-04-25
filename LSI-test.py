from numpy import zeros
from scipy.linalg import svd
#following needed for TFIDF
from math import log
from numpy import asarray, sum

titles = [ "Generalization and a Framework for Query Modification.",
          "Selectivity Estimation Using Homogeneity Measurement.",
          "Coupling hypertext to an object-oriented environment.",
          "Expert system support for the therapeutic management of cerebrovascular disease.",
          "Monitoring diseases with empirical and model-generated histories.",
          "Towards computer-assisted maintenance of medical knowledge bases.",
          "Expertext for medical care and literature retrieval.",
          "Parallel Linear Programming in Fixed Dimension Almost Surely in Constant Time",
          "Simple Constructions of Almost k-Wise Independent Random Variables",
          "Learning Conjunctions of Horn Clauses",
          "Communication-Optimal Maintenance of Replicated Information",
          "Network Synchronization with Polylogarithmic Overhead",
          "A Dining Philosophers Algorithm with Polynomial Response Time",
          "A Characterization of \sharp P Arithmetic Straight Line Programs",
          "Non-Deterministic Exponential Time Has Two-Prover Interactive Protocols"
          ]

stopwords = ['and','edition','for','in','little','of','the','to']
ignorechars = ''',:'!'''
#Define LSA Class
class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0        
# parsing the documents. Splits the document into words, removes the ignored characters and turns everything into lowercase. If the word is a stop word, it is ignored. If it is not a stop word, we put it in the dictionary. 
# The documents that each word appears in are kept in a list associated with that word in the dictionary. 
    def parse(self, doc):
        print "Adding doc", self.dcount, doc
        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
                print "\tadding doc", self.dcount, "to word,", w, ", doc list", self.wdict[w]
            else:
                self.wdict[w] = [self.dcount]
                print "\tadding doc", self.dcount, "to word,", w, ", doc list", self.wdict[w]
        self.dcount += 1  # increase the document count, for the next document to be parsed.    
# building the matrix of word counts. Once all documents are parsed, the words from more than 1 document are extracted and sorted. 
# Built the matrix with: 
# number of rows = the number of words (keys)
# number of columns = the document count. Finally, for each word (key) and document pair the corresponding matrix cell is increased.
    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
		#create (words_greater_than_one X docCount) matrix 
		# 		doc0	doc1	doc2	doc3	doc4	doc5	doc6	doc7	
		# w0 
		# w1 
		# w2
		# w3
		# w4 
		# ...
        print "matrix = ", len(self.keys), '(words) x ', self.dcount, "(document) matrix"
        self.A = zeros([len(self.keys), self.dcount])
        for word_idx, key in enumerate(self.keys):		#for each word
            for doc in self.wdict[key]:				#for each document
                self.A[word_idx, doc] += 1			#just add one, not the number of times it appears

    def calc(self):
        self.U, self.S, self.Vt = svd(self.A)
        uRows, uCols = self.U.shape
        sRows = self.S.shape
        vRows, vCols = self.Vt.shape
        print "U = ??? Matrix", uRows, 'x', uCols
        print "S = ??? Matrix", sRows
        print "V = ??? Matrix", vRows, 'x', vCols
# WordsPerDoc holds the total number of index words in each document. 
# DocsPerWord create an array with the number of documents in which word i appears. 
# Step through each cell and apply the formula.
    def TFIDF(self):
        WordsPerDoc = sum(self.A, axis=0)        
        DocsPerWord = sum(asarray(self.A > 0, 'i'), axis=1)
        rows, cols = self.A.shape
        for i in range(rows):
            for j in range(cols):
                self.A[i,j] = (self.A[i,j] / WordsPerDoc[j]) * log(float(cols) / DocsPerWord[i])

    def printA(self):
        print 'Here is the count matrix'
        print self.A

    def printSVD(self):
        print 'Here are the singular values, per document', len(self.S)
        print self.S
        print 'Here are the first 3 columns of the U matrix'
        print -1*self.U[:, 0:3]
        print 'Here are the first 3 rows of the Vt matrix'
        print -1*self.Vt[0:3, :]


mylsa = LSA(stopwords, ignorechars)

for t in titles:
    mylsa.parse(t)

mylsa.build()
#mylsa.TFIDF()
mylsa.printA()
mylsa.calc()
mylsa.printSVD()
