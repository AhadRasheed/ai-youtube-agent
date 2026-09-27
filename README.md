# AI YouTube Agent 

This is the cleaned, runnable Final V1 for the first local video sample.

## What it does

1. Ask for a topic.
2. Ask local Ollama for a content plan.
3. Search the web and read a small number of result pages.
4. Fact-check the collected research with Ollama.
5. Generate a script in four smaller requests.
6. Generate YouTube metadata.
7. Create a visual plan.
8. Create a real 1280x720 thumbnail PNG.
9. Create a real 1920x1080 H.264 MP4 using FFmpeg.

The sample video uses generated educational scene cards rather than
external AI images. This makes the first version reproducible without
a paid image-generation API or Piper TTS.

YouTube upload is deliberately not enabled in this V1.

## Requirements

Windows, Python 3.11+, Ollama, `llama3.2:3b`, internet access for
research, and FFmpeg.

FFmpeg must be available as:

```powershell
ffmpeg -version
```

Ollama must be available as:

```powershell
ollama list
```

and the model should include:

```text
llama3.2:3b
```

## Setup

From inside the project folder:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
ollama pull llama3.2:3b
python main.py
```

Choose:

```text
1
```

Then enter a topic.

The final MP4 will be:

```text
media\final\ai_youtube_agent_sample.mp4
```

The thumbnail will be:

```text
media\thumbnails\thumbnail.png
```

## Important

The first sample is an HD visual-card video. It proves the complete
topic -> research -> fact check -> script -> rendering pipeline.

Piper voice generation and YouTube publishing are separate future
steps and are not required to create the first MP4.
