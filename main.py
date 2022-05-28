from dataclasses import dataclass
from bs4 import BeautifulSoup
import urllib.request
import threading
import sys

@dataclass
class link:
    layer: int
    url: str

visited = set()

bad_sites = [
    "wiki/Wikipedia",
    "wikipedia_talk",
    "wikipedia:"
    "template",
    "help",
    "portal",
    "special",
    "category",
    "file",
    "user",
    "user_talk",
    "stats",
    "query", 
    "main",
    "donate",
    "wikimedia",
    "contact",
    "general",
    "content",
    "talk",
    "disclaimer",
    "about", 
    "license",
    "edit"
]

good_sites = [
    "en.m.wikipedia.org",

]

def UrlFilter(url):
    if url.startswith("//"):
        url = "http:" + url


    if url.startswith("/wiki/"):
        url = "https://en.m.wikipedia.org/" + url

    bad = False
    for site in bad_sites:
        if site in url.lower():
            bad = True
            break
    for site in good_sites:
        if site not in url.lower():
            bad = True
            break

    if url in visited:
        bad = True

    if not bad:
        return url
    else:
        return False

def findLinks(url1,lay:int):
    html = urllib.request.urlopen(url1)
    soup = BeautifulSoup(html, "html.parser")

    UrlList=[]
    for link1 in soup.findAll('a'):
        l = UrlFilter(str(link1.get('href')))
        if l:
            UrlList.append(link(lay, l))

    return UrlList

act_layer = []
next_layer = []

found = False

def expandingGraph(n, endUrl): #takes link and putts all the links to queue (next_layer list)
    global act_layer 
    global next_layer 
    global found

    if n.url == endUrl:
        print("FOUND!\nFOUND!", n.url, endUrl)
        found = True
        return n.layer
    try:
        next_layer.extend(findLinks(n.url, n.layer+1))
        print(n.url, " visited ", n.layer)

    except:
        print("couldn't open: ", n.url)
    visited.add(n.url)
    

def bfs(startingUrl, endUrl):

    global act_layer
    global next_layer 
    global found

    act_layer.append(link(0,startingUrl))
    while True:
        thread_list = []

        for n in act_layer:
            thread_list.append(threading.Thread(target=expandingGraph, args=(n, endUrl)))

        i = 0
        last = 0
        while i < len(thread_list):
            act_layer.pop(0)
            thread_list[i].start()

            if i%10==0:
                while last<i:
                    thread_list[last].join()
                    last=last+1
            if found:
                return 0
            i=i+1        
        
        act_layer=next_layer.copy()
        next_layer.clear()
        thread_list.clear()
        i=0
        
        

print(bfs("http://en.m.wikipedia.org/wiki/flags","https://en.m.wikipedia.org/wiki/Banner")) #flags -> halophyte - 4 links

