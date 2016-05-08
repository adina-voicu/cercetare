import csv
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
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
# lemmatize text         
def lemma(txt):
    a=[]
    for i in txt:
        x = ' '.join([wnl.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_tag(word_tokenize(i))])
        a.append(x)
    return a
#remove stopwords
def stop(txt):
    x=[]
    for w in txt.split():
        if w not in stopwords:
            x.append(w)
        else:
            continue
    return ' '.join(x)

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
    print output
