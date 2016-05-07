import csv
with open('datec.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    header= [ 'id', 'conf', 'title', 'author', 'year', 'abstract', 'eq', 'conf_short', 'theme']
    output=[]
    for line in reader:
        row={}
        for field in header:
            row[field]=line[field]
        output.append(row)
    print output
        

