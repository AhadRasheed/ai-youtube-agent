import json
from datetime import datetime
from agent.ai_brain import ask_ollama
from config import METADATA_DIR

def generate_metadata(topic,script):
    prompt=f'''Generate YouTube metadata.
Topic: {topic}
Script: {json.dumps(script,ensure_ascii=False)}
Return ONLY JSON: {{"title":"...","description":"...","tags":["...","...","..."]}}'''
    result=ask_ollama(prompt)
    path=METADATA_DIR/f"metadata_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
    path.write_text(json.dumps(result,indent=4,ensure_ascii=False),encoding="utf-8")
    return result,str(path)
