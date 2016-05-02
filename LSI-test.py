from numpy import zeros
from scipy.linalg import svd
from nltk.corpus import stopwords
from math import log
from numpy import asarray, sum
import nltk
from gensim import corpora, models, similarities

titles = [ "A Query Algebra for Object-Oriented Databases.	We define an algebra that synthesizes relational query concepts with object-oriented databases. The algebra fully supports abstract data types and object identity while providing associative access to objects, including a unique join capability. The operations take an abstract view of objects and access typed collections of objects through the public interface defined for the type. The algebra supports access to relationships implied by the structure of the objects, as well as the definition and creation of new relationships between objects. The structure of the algebra and the abstract access to objects offer opportunities for query optimization.",
"A Modular Query Optimizer Generator.",	
"Currency-Based Updates to Distributed Materialized Views.A Query Algebra for Object-Oriented Databases.	We define an algebra that synthesizes relational query concepts with object-oriented databases. The algebra fully supports abstract data types and object identity while providing associative access to objects, including a unique join capability. The operations take an abstract view of objects and access typed collections of objects through the public interface defined for the type. The algebra supports access to relationships implied by the structure of the objects, as well as the definition and creation of new relationships between objects. The structure of the algebra and the abstract access to objects offer opportunities for query optimization.",
"A Modular Query Optimizer Generator.",
"Currency-Based Updates to Distributed Materialized Views.",	
"Extended Relations.",	
"The Semantic Data Model for Security: Representing the Security Semantics of an Application.",	
"Performance Evaluation of Multiversion Database Systems.",	
"Parallelism in Database Production Systems.",
"Distributed RAID - A New Multiple Copy Algorithm.",
"Supporting Universal Quantification in a Two-Dimensional Database Query Language."	
"The Fingerprinted Database.",
"Concurrency Control Using Locking with Deferred Blocking.",	
"Experiences with Distributed Query Processing.	",
"Efficient Updates to Independent Schemes in the Weak Instance Model.	The weak instance model is a framework to consider the relations in a database as a whole, regardless of the way attributes are grouped in the individual relations. Queries and updates can be performed involving any set of attributes. The management of updates is based on a lattice structure on the set of legal states, and inconsistencies and ambiguities can arise In the general case, the test for inconsistency and determinism may involve the application of the chase algorithm to the whole database. In this paper it is shown how, for the highly significant class of independent schemes, updates can be handled efficiently, considering only the relevant portion of the database.",
"OdeView: The Graphical Interface to Ode.	OdeView is the graphical front end for Ode, an object-oriented database system and environment. Ode's data model supports data encapsulation, type inheritance, and complex objects. OdeView provides facilities for examining the database schema (i.e., the object type or class hierarchy), examining class definitions, browsing objects, following chains of references starting from an object, synchronized browsing, displaying selected portions of objects (projection), and retrieving objects with specific characteristics (selection). OdeView does not need to know about the internals of Ode objects. Consequently, the internals of specific classes are not hardwired into OdeView and new classes can be added to the Ode database without requiring any changes to or recompilation of OdeView. Just as OdeView does not know about the object internals, class functions (methods) for displaying objects are written without knowing about the specifics of the windowing software used by OdeView or the graphical user interface provided by it. In this paper, we present OdeView, and discuss its design and implementation.",

"The Object-Oriented Database System Manifesto.",	
"'Performance Evaluation of Semantics-based Multilevel Concurrency Control Protocols.	For next generation information systems, concurrency control mechanisms are required to handle high level abstract operations and to meet high throughput demands. The currently available single level concurrency control mechanisms for reads and writes are inadequate for future complex information systems. In this paper, we will present a new multilevel concurrency protocol that uses a semantics-based notion of conflict, which is weaker than commutativity, called recoverability. Further, operations are scheduled according to relative conflict, a conflict notion based on the structure of operations. Performance evaluation via extensive simulation studies show that with our multilevel concurrency control protocol, the performance improvement is significant when compared to that of a single level two-phase locking based concurrency control scheme or to that of a multilevel concurrency control scheme based on commutativity alone. Further, simulation studies show that our new multilevel concurrency control protocol performs better even with resource contention.",
"Implementing Recoverable Requests Using Queues.	Transactions have been rigorously defined and extensively studied in the database and transaction processing literature, but little has been said about the handling of the requests for transaction execution in commercial TP systems, especially distributed ones, managing the flow of requests is often as important as executing the transactions themselves. This paper studies fault-tolerant protocols for managing the flow of transaction requests between clients that issue requests and servers that process them. We discuss how to implement these protocols using transactions and recoverable queuing systems. Queuing systems are used to move requests reliably between clients and servers. The protocols use queuing systems to ensure that the server processes each request exactly once and that a client processes each reply at least once. We treat request-reply protocols for single-transaction requests, for multi-transaction requests, and for requests that require interaction with the display after the request is submitted.",
"The R*-Tree: An Efficient and Robust Access Method for Points and Rectangles.	The R-tree, one of the most popular access methods for rectangles, is based on the heuristic optimization of the area of the enclosing rectangle in each inner node. By running numerous experiments in a standardized testbed under highly varying data, queries and operations, we were able to design the R*-tree which incorporates a combined optimization of area, margin and overlap of each enclosing rectangle in the directory. Using our standardized testbed in an exhaustive performance comparison, it turned out that the R*-tree clearly outperforms the existing R-tree variants. Guttman's linear and quadratic R-tree and Greene's variant of the R-tree. This superiority of the R*-tree holds for different types of queries and operations, such as map overlay, for both rectangles and multidimensional points in all experiments. From a practical point of view the R*-tree is very attractive because of the following two reasons 1 it efficiently supports point and spatial data at the same time and 2 its implementation cost is only slightly higher than that of other R-trees.",
"Reliable Transaction Management in a Multidatabase System.	A model of a multidatabase system is defined in which each local DBMS uses the two-phase locking protocol Locks are released by a global transaction only after the transaction commits or aborts at each local site. Failures may occur during the processing of transactions. We design a fault tolerant transaction management algorithm and recovery procedures that retain global database consistency. We also show that our algorithms ensure freedom from global deadlocks of any kind.",
"Integrating Object-Oriented Data Modeling with a Rule-Based Programming Paradigm.	LOGRES is a new project for the development of extended database systems which is based on the integration of the object-oriented data modelling paradigm and of the rule-based approach for the specification of queries and updates. The data model supports generalization hierarchies and object sharing, the rule-based language extends Datalog to support generalized type constructors (sets, multisets, and sequences), rule-based integrity constraints are automatically produced by analyzing schema definitions. Modularization is a fundamental feature, as modules encapsulate queries and updates, when modules are applied to a LOGRES database, their side effects can be controlled. The LOGRES project is a follow-up of the ALGRES project, and takes advantage of the ALGRES programming environment for the development of a fast prototype.",
"ACTA: A Framework for Specifying and Reasoning about Transaction Structure and Behavior.	Recently, a number of extensions to the traditional transaction model have been proposed to support new information-intensive applications such as CAD/CAM and software development. However, these extended models capture only a subset of interactions that can be found in such applications, and represent only some of the points within the spectrum of interactions possible in competitive and cooperative environments. ACTA is a formalizable framework developed for characterizing the whole spectrum of interactions. The ACTA framework is not yet another transaction model, but is intended to unify the existing models. ACTA allows for specifying the structure and the behavior of transactions as well as for reasoning about the concurrency and recovery properties of the transactions. In ACTA, the semantics of interactions are expressed in terms of transactions' effects on the commit and abort of other transactions and on objects' state and concurrency status (i.e., synchronization state). Its ability to capture the semantics of previously proposed transaction models is indicative of its generality. The reasoning capabilities of this framework have also been tested by using the framework to study the properties of a new model that is derived by combining two existing transaction models.",
"Organizing Long-Running Activities with Triggers and Transactions.	This paper addresses the problem of organising and controlling activities that involve multiple steps of processing and that typically are of long duration. We explore the use of triggers and transactions to specify and organize such long-running activities. Triggers offer data- or event-driven specification of control flow, and thus provide a flexible and modular framework with which the control structures of the activities can be extended or modified. We describe a model based on event-condition-action rules and coupling modes. The execution of these rules is governed by an extended nested transaction model. Through a detailed example, we illustrate the utility of the various features of the model for chaining related steps without sacrificing concurrency, for enforcing integrity constraints, and for providing flexible failure and exception handling.",
"Encapsulation of Parallelism in the Volcano Query Processing System.	Volcano is a new dataflow query processing system we have developed for database systems research and education. The uniform interface between operators makes Volcano extensible by new operators. All operators are designed and coded as if they were meant for a single-process system only. When attempting to parallelize Volcano, we had to choose between two models of parallelization, called here the bracket and operator models. We describe the reasons for not choosing the bracket model, introduce the novel operator model, and provide details of Volcano's exchange operator that parallelizes all other operators. It allows intra-operator parallelism on partitioned datasets and both vertical and horizontal inter-operator parallelism. The exchange operator encapsulates all parallelism issues and therefore makes implementation of parallel database algorithms significantly easier and more robust. Included in this encapsulation is the translation between demand-driven dataflow within processes and data-driven dataflow between processes. Since the interface between Volcano operators is similar to the one used in &ldquo;real,&rdquo; commercial systems, the techniques described here can be used to parallelize other query processing engines.",
"A Framework for the Parallel Processing of Datalog Queries.	This paper presents several complementary methods for the parallel, bottom-up evaluation of Datalog queries. We introduce the notion of a discriminating predicate, based on hash functions, that partitions the computation between the processors in order to achieve parallelism. A parallelization scheme with the property of non-redundant computation (no duplication of computation by processors) is then studied in detail. The mapping of Datalog programs onto a network of processors, such that the results is a non-redundant computation, is also studied. The methods reported in this paper clearly demonstrate the trade-offs between redundancy and interprocessor-communication for this class of problems.",
"A Graph-Oriented Object Model for Database End-User Interfaces.",	
"A Predicate Matching Algorithm for Database Rule Systems.	Forward-chaining rule systems must test each newly asserted fact against a collection of predicates to find those rules that match the fact. Expert system rule engines use a simple combination of hashing and sequential search for this matching. We introduce an algorithm for finding the matching predicates that is more efficient than the standard algorithm when the number of predicates is large. We focus on equality and inequality predicates on totally ordered domains. This algorithm is well-suited for database rule systems, where predicate-testing speed is critical. A key component of the algorithm is the interval binary search tree (IBS-tree). The IBS-tree is designed to allow efficient retrieval of all intervals (e.g. range predicates) that overlap a point, while allowing dynamic insertion and deletion of intervals. The algorithm could also be used to improve the performance of forward-chaining inference engines for large expert systems applications.",
"Randomized Algorithms for Optimizing Large Join Queries.	Query optimization for relational database systems is a combinatorial optimization problem, which makes exhaustive search unacceptable as the query size grows. Randomized algorithms, such as Simulated Annealing (SA) and Iterative Improvement (II), are viable alternatives to exhaustive search. We have adapted these algorithms to the optimization of project-select-join queries. We have tested them on large queries of various types with different databases, concluding that in most cases SA identifies a lower cost access plan than II. To explain this result, we have studied the shape of the cost function over the solution space associated with such queries and we have conjectured that it resembles a 'cup' with relatively small variations at the bottom. This has inspired a new Two Phase Optimization algorithm, which is a combination of Simulated Annealing and Iterative Improvement. Experimental results show that Two Phase Optimization outperforms the original algorithms in terms of both output quality and running time.",
"Linear Clustering of Objects with Multiple Atributes.	There is often a need to map a multi-dimensional space on to a one-dimensional space. For example, this kind of mapping has been proposed to permit the use of one-dimensional indexing techniques to a multi-dimensional index space such as in a spatial database. This kind of mapping is also of value in assigning physical storage, such as assigning buckets to records that have been indexed on multiple attributes, to minimize the disk access effort. In this paper, we discuss what the desired properties of such a mapping are, and evaluate, through analysis and simulation, several mappings that have been proposed in the past. We present a mapping based on Hilbert's space-filling curve, which out-performs previously proposed mappings on average over a variety of different operating conditions."
          ]
stopwords = nltk.corpus.stopwords.words('english')
ignorechars = ''',:'!()'''
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
    def token(self, doc): 
        texts = [[word for word in doc.lower().split() if word not in self.stopwords]
          for d in doc]
#doc2bow converts a collection of words to its bag-of-words representation: a list of (word_id, word_frequency)
        dictionary = corpora.Dictionary(texts)
        #corpus = [dictionary.doc2bow(word) for word in texts]
        corpus = (dictionary.doc2bow(tokenize_func(document)) for document in titles)
        #print (dictionary)  
        print corpus,    
        index = dict((v, k) for k, v in dictionary.token2id.iteritems())
        #print index
        print(dictionary.token2id)
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
            for doc in self.wdict[key]:					#for each document
                self.A[word_idx, doc] += 1				#just add one, not the number of times it appears

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


mylsa = LSA(stopwords, ignorechars)

for t in titles:
    mylsa.parse(t)

mylsa.build()
#mylsa.TFIDF()
for w in titles:
    mylsa.token(w)
mylsa.printA()
