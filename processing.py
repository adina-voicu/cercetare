#! /usr/bin/python

import csv
#import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import nltk
from nltk.tokenize import word_tokenize
from pymongo import MongoClient
import pymongo
from collections import defaultdict
import sys  

reload(sys)
sys.setdefaultencoding('utf8')

wnl = WordNetLemmatizer()
documents = "A key to developing computationally efficient stereo vision is the incorporation of intelligent control. Stereo is most effective when it is able to focus its analysis on regions and details of a scene that are important to the task at hand, while avoiding less important regions and unnecessary detail. The paper describes two methods for electronically focusing stereo measurement through simple image pre-processing. The first allows measurement sensitivity to be adjusted. The second allows the shape of the 3D region in which measurements are gathered to be matched to the shape of surfaces in the scene.Recognition systems attempt to recover information about the identity of the observed objects and their location in the environment. A fundamental problem in recognition is the following. Given a correspondence between some portions of an object model and some portions of an image, determine whether the image contains an instance of the object, and, in case it does, determine the transformation that relates the model to the image. The current approaches to this problem are divided into methods that use global properties of the object (e.g., centroid and moments of inertia) and methods that use local properties of the object (e.g., corners and line segments). Global properties are sensitive to occlusion and, specifically, to self occlusion. Local properties are difficult to locate reliably, and their matching involves intensive computation. A novel method for recognition that uses region information is presented. In our approach the model is divided into volumes, and the image is divided into regions. Given a match between subsets of volumes and regions (without any explicit correspondence between different pieces of the regions) the alignment transformation is computed. The method applies to planar objects under similarity, affine, and projective transformations and to projections of 3-D objects undergoing affine and projective transformations. The new approach combines many of the advantages of the previous two approaches, while avoiding some of their pitfalls. Like the global methods, our approach makes use of region information that reflects the true shape of the object. But like local methods, our approach can handle occlusion.A new method for representing and recognizing human body movements is presented. The basic idea is to identify sets of constraints that are diagnostic of a movement: expressed using body-centered coordinates such as joint angles and in force only during a particular movement. Assuming the availability of Cartesian tracking data, we develop techniques for a representation of movements defined by space curves in subspaces of a phase space. The phase space has axes of joint angles and torso location and attitude, and the axes of the subspaces are subsets of the axes of the phase space. Using this representation we develop a system for learning new movements from ground truth data by searching for constraints. We then use the learned representation for recognizing movements in unsegmented data. We train and test the system on nine fundamental steps from classical ballet performed by two dancers; the system accurately recognizes the movements in the unsegmented stream of motion. We deal with the calibration problem of an active head-eye system, which consists of a pair of cameras mounted on a head with 13 degrees of freedom. The aim of the calibration is to establish relative positions of different 3D systems: between camera and neck, eye and neck, etc., so that we can keep track of the camera position in a fixed (calibration) reference system as a function of the visual parameters of the head-eye system. We formulate the problem and propose both closed-form and nonlinear optimization approaches to solve it. Experiments were carried out and comparison of results with other algorithms were made on both simulated and real data."

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
		return tag
def lemma(sentences):
	z = []
	for sentence in sentences:
		for word, tag in pos_tag(word_tokenize(sentence)):
			if clean_sentence(word) == '':
				x = (word, 'clean')
			elif pos(tag) in ['n', 'v', 'a', 'r']:
				x = (wnl.lemmatize(word, pos(tag)), pos(tag))  
			else:
				x = (word, tag)
			z.append(x)
	return z


grammar = {
			"P1": "P1: {<n>}",
			"P2": "P2: {<n> <n>}",
			"P3": "P3: {<a> <n>}",
			"P4": "P4: {<a> <n> <n>}",
			"P5": "P5: {<a> <a> <n>}",
			"P6": "P6: {<n> <a> <n>}"
		}

def filter(prop):
	filttags = []
	for sent in prop:
		for g in grammar:		
			cp = nltk.RegexpParser(grammar[g])
			result = cp.parse(sent) 
			filttags.append(result) # create a tree with chunks with pos like grammar and the rest of words
	return filttags

def clean(str):
	str = ''.join([c for c in str \
		if c in 'ABCDEFGHIJKLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz- \''])
	str = str.replace('  ', ' ')
	return str
def clean_sentence(s):
	str = ''
	for word in s:
		lst_cleaned = []
		for items in s:
			str += ' '.join(clean(items))
			#str = str.replace('- ', '')
		return str

def ngrams(tree_list):
	y = {}
	
	for tree in tree_list:
		#print(tree)
		for subtree in tree.subtrees():
			for g in grammar:
				if subtree.label() == g:
					if clean_sentence(' '.join(tuple(word[0] for word in subtree))) not in y.keys():
						y[clean_sentence(' '.join(tuple(word[0] for word in subtree)))] = 1
					else:
						y[clean_sentence(' '.join(tuple(word[0] for word in subtree)))] += 1
	return y

def terms(tuplist):
	s = ''
	s = s + ' '.join(a for (a,b) in tuplist)
	return clean_sentence(s)
	
def insert(docs):
	con = pymongo.MongoClient()
	coll = con.documents.docs
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
i = 0		
with open('dataconf_prep.csv') as csvf:
	reader = csv.DictReader(csvf, delimiter='	')
	header = ['id', 'conf', 'title', 'author', 'year', 'abstract', 'conf_short', 'theme']
	output = []
	fq = {}
	for line in reader:
		row = {}
		for field in header:
			if field == 'abstract':
				row['abstract'] = line[field]
				row['ngrams'] = ngrams(filter([lemma(nltk.sent_tokenize(line['abstract'].lower()))]))
				row['terms'] = terms(lemma(nltk.sent_tokenize(line['abstract'].lower())))
			else:
				row[field] = line[field]
		output.append(row)
	insert(output)
