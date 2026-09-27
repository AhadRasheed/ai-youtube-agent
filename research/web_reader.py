from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def read_url(url,max_chars=8000):
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; AIYouTubeAgent/1.0)"})
    with urlopen(req,timeout=20) as r:
        html=r.read()
    soup=BeautifulSoup(html,"html.parser")
    for tag in soup(["script","style","noscript"]):
        tag.decompose()
    return soup.get_text(" ",strip=True)[:max_chars]
