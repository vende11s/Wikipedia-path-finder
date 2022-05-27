from dataclasses import dataclass
from bs4 import BeautifulSoup
import urllib.request

@dataclass
class link:
    layer: int
    url: str

visited = []

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

    for site in visited:
        if site in url.lower():
            bad = True
            break

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


def bfs(startingUrl, endUrl):
    counter = 0
    act_layer = []
    next_layer = []
    act_layer.append(link(0,startingUrl))
    while act_layer:
        n = act_layer[0]
        act_layer.pop(0)

        if n.layer > counter:
            coutner=counter+1

        if n.url == endUrl:
            return counter    

        if not act_layer:
            act_layer = next_layer.copy()
            next_layer.clear()

        try:
            next_layer.extend(findLinks(n.url, n.layer+1))
            print(n.url, " visited ", n.layer)

        except:
            print("couldn't open: ", n.url)
        visited.append(n.url)


print(bfs("http://en.m.wikipedia.org/wiki/flags","https://en.m.wikipedia.org//wiki/Brigade"))

