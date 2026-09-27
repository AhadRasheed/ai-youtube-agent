from datetime import datetime

from agent.ai_brain import ask_ollama
from agent.topic_manager import get_topic
from agent.researcher import research_topic
from agent.fact_checker import fact_check
from agent.script_writer import write_script
from agent.metadata_generator import generate_metadata
from agent.visual_generator import create_visual_plan
from agent.thumbnail_generator import create_thumbnail
from agent.video_editor import render_video
from config import TOPICS_DIR


def run_agent():
    print("\n========================================")
    print("        AI YOUTUBE AGENT - V1")
    print("========================================")

    topic = get_topic()
    if not topic:
        print("No topic selected. Exiting.")
        return

    topic_path = TOPICS_DIR / f"topic_{datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
    topic_path.write_text(topic, encoding="utf-8")

    print("\n[1/8] AI content plan...")
    plan = ask_ollama(
        f"""Create a YouTube educational content plan for this topic:
{topic}

Return ONLY valid JSON:
{{
  "audience": "...",
  "content_goal": "...",
  "video_angle": "...",
  "research_needed": ["...", "...", "..."],
  "suggested_sections": ["...", "...", "...", "..."]
}}"""
    )

    print("[2/8] Internet research...")
    research, rpath = research_topic(
        topic,
        plan.get("research_needed", []) if isinstance(plan, dict) else [],
    )
    print("Research:", rpath)

    print("[3/8] Fact checking...")
    facts, fpath = fact_check(topic, research)
    print("Fact check:", fpath)

    print("[4/8] Script writing...")
    script, spath = write_script(topic, plan, research, facts)
    print("Script:", spath)

    print("[5/8] Metadata...")
    metadata, mpath = generate_metadata(topic, script)
    print("Metadata:", mpath)

    print("[6/8] Visual planning...")
    visual_path = create_visual_plan(script)
    print("Visual plan:", visual_path)

    print("[7/8] Thumbnail...")
    thumbnail_path = create_thumbnail(metadata.get("title", topic))
    print("Thumbnail:", thumbnail_path)

    print("[8/8] HD video rendering...")
    video_path = render_video(
        script=script,
        title=metadata.get("title", topic),
    )
    print("Final video:", video_path)

    print("\n========================================")
    print("VIDEO CREATION COMPLETE")
    print("========================================")
    print("Topic:", topic)
    print("MP4:", video_path)
    print("Thumbnail:", thumbnail_path)
    print("The video is a 1920x1080 visual-card sample with on-screen narration excerpts.")
    print("YouTube uploading remains disabled in this V1.")
