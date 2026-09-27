import json
from datetime import datetime
from config import ANALYTICS_DIR

def save_upload_result(result):
    path=ANALYTICS_DIR/f"upload_{datetime.now():%Y-%m-%d_%H-%M-%S}.json"
    path.write_text(json.dumps(result,indent=4),encoding="utf-8")
    return str(path)
