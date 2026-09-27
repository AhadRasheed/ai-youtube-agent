from pathlib import Path

def check_credentials():
    path=Path("credentials/client_secret.json")
    if not path.exists():
        raise RuntimeError("Put Google OAuth client JSON at credentials/client_secret.json.")
    return path
