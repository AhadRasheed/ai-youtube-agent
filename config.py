from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
TOPICS_DIR = DATA_DIR / "topics"
RESEARCH_DIR = DATA_DIR / "research"
SCRIPTS_DIR = DATA_DIR / "scripts"
METADATA_DIR = DATA_DIR / "metadata"
ANALYTICS_DIR = DATA_DIR / "analytics"
MEDIA_DIR = BASE_DIR / "media"
AUDIO_DIR = MEDIA_DIR / "audio"
IMAGES_DIR = MEDIA_DIR / "images"
VIDEOS_DIR = MEDIA_DIR / "videos"
THUMBNAILS_DIR = MEDIA_DIR / "thumbnails"
FINAL_DIR = MEDIA_DIR / "final"
LOGS_DIR = BASE_DIR / "logs"
CREDENTIALS_DIR = BASE_DIR / "credentials"

for d in [TOPICS_DIR,RESEARCH_DIR,SCRIPTS_DIR,METADATA_DIR,ANALYTICS_DIR,
          AUDIO_DIR,IMAGES_DIR,VIDEOS_DIR,THUMBNAILS_DIR,FINAL_DIR,LOGS_DIR,CREDENTIALS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = os.getenv("OLLAMA_URL","http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL","llama3.2:3b")
