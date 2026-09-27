import json
from datetime import datetime
from config import RESEARCH_DIR
from research.search import search_web
from research.web_reader import read_url

def research_topic(topic,research_questions):
    sources=[]
    for query in [topic]+research_questions[:3]:
        try:
            results=search_web(query,3)
        except Exception as e:
            sources.append({"query":query,"error":str(e),"results":[]})
            continue
        for result in results:
            item=dict(result)
            try: item["content"]=read_url(result["url"])
            except Exception as e: item["content"]=""; item["read_error"]=str(e)
            sources.append(item)
    data={"topic":topic,"created_at":datetime.now().isoformat(),"sources":sources}
    path=RESEARCH_DIR/f"research_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
    path.write_text(json.dumps(data,indent=4,ensure_ascii=False),encoding="utf-8")
    return data,str(path)
