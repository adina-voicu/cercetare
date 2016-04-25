from numpy import zeros
from scipy.linalg import svd

titles = ["Generalization and a Framework for Query Modification."
          "Selectivity Estimation Using Homogeneity Measurement." 
          "Coupling hypertext to an object-oriented environment."
          "Expert system support for the therapeutic management of cerebrovascular disease."
          "Making deepness explicit."
          "Monitoring diseases with empirical and model-generated histories."
          "Towards computer-assisted maintenance of medical knowledge bases."
          "Expertext for medical care and literature retrieval."
          "Parallel Linear Programming in Fixed Dimension Almost Surely in Constant Time"
          "Uniform Memory Hierarchies"
          "Simple Constructions of Almost k-Wise Independent Random Variables"
          "Learning Conjunctions of Horn Clauses (Extended Abstract)"
          "Fault Tolerant Sorting Network"
          "Are Wait-Free Algorithms Fast? (Extended Abstract)"
          "Communication-Optimal Maintenance of Replicated Information"
          "Sparse Partitions (Extended Abstract)"
          "Network Synchronization with Polylogarithmic Overhead"
          "A Dining Philosophers Algorithm with Polynomial Response Time"
          "A Characterization of \sharp P Arithmetic Straight Line Programs"
          "Non-Deterministic Exponential Time Has Two-Prover Interactive Protocols"
]
stopwords = ['a','and','edition','for','in','little','of','the','to']
ignorechars = ''',:'!'''

#Define LSA Class

class LSA(object):
#method for initialization, it stores the stopwords and ignorechars, and then initializes the word dictionary and the document count variables.
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0
# parsing the documents. Splits the document into words, removes the ignored characters and turns everything into lowercase. If the word is a stop word, it is ignored. If it is not a stop word, we put it in the dictionary. 
# The documents that each word appears in are kept in a list associated with that word in the dictionary.     
    def parse(self, doc):
        words = doc.split();
        for w in words:
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1  # increase the document count, for the next document to be parsed.
        print(self.wdict)
# building the matrix of word counts. Once all documents are parsed, the words from more than 1 document are extracted and sorted. 
# Built the matrix with: 
# number of rows = the number of words (keys)
# number of columns = the document count. Finally, for each word (key) and document pair the corresponding matrix cell is increased.
    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
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
# prints out the matrix that we have built so it can be checked
    def printA(self):
        print ('Here is the count matrix')
        print (self.A)
 
# Test the LSA Class        
mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)   # call the parse method on each title
mylsa.build()    # create the matrix of word by title counts.
mylsa.printA()   # print the matrix
