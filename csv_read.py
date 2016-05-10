import csv
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import pymongo
from pymongo import MongoClient

wnl = WordNetLemmatizer()
#obtain a clean sentence
def clean(str):
    str = ''.join([c for c in str if c in 'ABCDEFGHIJKLNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 \''])
    return str
def clean_sentence(s):
    for word in s:
        lst_cleaned = []
        for items in s:
            lst_cleaned.append(clean(items))
        return lst_cleaned

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

# lemmatize text         
def lemma(sentences):
    a=[]
    for sentence in sentences:
        x = ' '.join([wnl.lemmatize(word, pos(tag)) for word, tag in pos_tag(word_tokenize(sentence)) if pos(tag) in ['n', 'v', 'a', 'r'] ])

        a.append(x)
    return a
#remove stopwords
def stop(txt):
    stopwords = nltk.corpus.stopwords.words('english')
    x=[]
    for w in txt.split():
        if w not in stopwords:
            x.append(w)
        else:
            continue
    return ' '.join(x)
#insert docs in mongodb
def insert(docs):
    con = pymongo.MongoClient()
    coll = con.test.contacts
    for doc in docs:
        coll.save(doc)

with open('datec.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    header= [ 'id', 'conf', 'title', 'author', 'year', 'abstract', 'eq', 'conf_short', 'theme']
    output=[]
    for line in reader:
        row={}
        for field in header:
            if field == 'abstract':
                row['abstract'] = stop(' '.join(lemma(clean_sentence(nltk.sent_tokenize(line['abstract'])))))
            else:    
                row[field]=line[field]
        output.append(row)
    insert(output)
    print output
