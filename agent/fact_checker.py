import json
from datetime import datetime
from agent.ai_brain import ask_ollama
from config import RESEARCH_DIR

def fact_check(topic,research):
    sources=[{"title":s.get("title",""),"url":s.get("url",""),
              "snippet":s.get("snippet",""),"content":s.get("content","")[:1800]}
             for s in research.get("sources",[])[:12]]
    prompt=f'''Topic: {topic}
Research sources:
{json.dumps(sources,ensure_ascii=False)}
Return ONLY JSON:
{{"claims":[{{"claim":"...","status":"supported|uncertain|conflicting",
"evidence":"...","source_urls":["..."]}}],"safe_summary":"..."}}
Do not invent evidence.'''
    result=ask_ollama(prompt)
    path=RESEARCH_DIR/f"fact_check_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
    path.write_text(json.dumps(result,indent=4,ensure_ascii=False),encoding="utf-8")
    return result,str(path)
