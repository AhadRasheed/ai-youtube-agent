from urllib.parse import quote
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def search_web(query, max_results=5):
    url="https://www.bing.com/search?q="+quote(query)
    req=Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; AIYouTubeAgent/1.0)"})
    with urlopen(req,timeout=20) as r:
        html=r.read()
    soup=BeautifulSoup(html,"html.parser")
    out=[]
    for item in soup.select("li.b_algo")[:max_results]:
        a=item.select_one("h2 a")
        p=item.select_one(".b_caption p")
        if a:
            out.append({"title":a.get_text(" ",strip=True),
                        "url":a.get("href",""),
                        "snippet":p.get_text(" ",strip=True) if p else ""})
    return out
