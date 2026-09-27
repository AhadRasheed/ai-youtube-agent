import json
from config import IMAGES_DIR


def create_visual_plan(script):
    """Create a readable scene plan from the generated script."""
    scenes = []
    sections = script.get("sections", []) if isinstance(script, dict) else []

    for index, section in enumerate(sections, start=1):
        narration = section.get("narration", "")
        scenes.append(
            {
                "scene": index,
                "title": section.get("section_title", f"Section {index}"),
                "visual_type": "educational_text_card",
                "visual_prompt": (
                    f"HD educational visual for: "
                    f"{section.get('section_title', f'Section {index}')}"
                ),
                "narration": narration,
            }
        )

    path = IMAGES_DIR / "visual_plan.json"
    path.write_text(
        json.dumps(scenes, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    text_path = IMAGES_DIR / "visual_plan.txt"
    lines = []
    for scene in scenes:
        lines.append(
            f"SCENE {scene['scene']}\n"
            f"TITLE: {scene['title']}\n"
            f"VISUAL: {scene['visual_prompt']}\n"
            f"NARRATION: {scene['narration']}\n"
        )
    text_path.write_text("\n".join(lines), encoding="utf-8")
    return path
