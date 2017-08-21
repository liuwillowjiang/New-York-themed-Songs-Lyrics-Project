import nltk,urllib, urllib2,requests,bs4,sys
from bs4 import BeautifulSoup


site='http://www.mldb.org/'


def getlinks(pageLink):
    print("------ Read url of page: {}".format(pageLink))
    response=urllib2.urlopen(pageLink)
    html=response.read()
    htmlsoup=BeautifulSoup(html,'html.parser')
    type(htmlsoup)
    table=htmlsoup.find('table', attrs={"id":"thelist"})
    first_td=table.findAll("td", { 'class': 'ft'})

    links=[]
    for item in first_td:
        links.append(str(item.find('a')['href']))

    #print links
    return links

response=urllib2.urlopen(site + 'search?mq=new+york&si=2&mm=0&ob=1')
html=response.read()
htmlsoup=BeautifulSoup(html,'html.parser')

pages_a = htmlsoup.find('div', attrs={'align':"center", 'style':"width:596px;"}).findAll('a')

allLinks=[]
allLinks.extend(getlinks(site + 'search?mq=new+york&si=2&mm=0&ob=1'))
for i in pages_a:
    pageLink = str(i['href'])
    links = getlinks(site + pageLink)
    allLinks.extend(links)

print("\n\n\n")

combinedLyrics = ""
for link in allLinks:
    print("------ Read url of song: {}".format(link))
    response=urllib2.urlopen(site + link)
    html=response.read()
    htmlsoup=BeautifulSoup(html,'html.parser')
    
    lyrics = htmlsoup.find('p', {'class':'songtext'}).text.replace('\n', ' ').encode('utf-8').strip()
    combinedLyrics += lyrics
    
f = lambda x: '' if (ord(x) > 127) else x
temp = map(f, combinedLyrics)
combinedLyrics_cleaned = ''.join(temp)

print("----- Tokenizing")
tokens=nltk.word_tokenize(combinedLyrics_cleaned)

#print (combinedLyrics)

print("------ Creating bigram")
bgs=nltk.bigrams(tokens)

print("------ Creating Frequency")
fdist=nltk.FreqDist(bgs)

print("\n\n\n")
for k,v in fdist.items():
    print (k,v)

print("--------------------sorted result")
bigramrank=sorted(fdist.items(), key=lambda x: x[1], reverse=True)
for (k,v) in bigramrank:
    print (k,v)

