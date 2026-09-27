import json
from datetime import datetime
from pathlib import Path

from .ai_brain import ask_ollama


# Number of script sections.
SECTION_COUNT = 4


def _limit_text(value, max_chars):
    """
    Prevent extremely large research/context data from being
    sent to the local 3B model.
    """

    if value is None:
        return ""

    if isinstance(value, (dict, list)):
        text = json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
        )
    else:
        text = str(value)

    if len(text) > max_chars:
        return text[:max_chars] + "\n...[context truncated]..."

    return text


def _get_field(data, field, default=""):
    """
    Safely get a field from a dictionary.
    """

    if isinstance(data, dict):
        return data.get(field, default)

    return default


def _generate_section(
    topic,
    plan,
    research,
    fact_check,
    section_number,
    section_title,
):
    """
    Generate one smaller part of the YouTube script.

    Smaller requests are easier for a local 3B model to complete
    than one huge 5-7 minute script request.
    """

    research_text = _limit_text(research, 5000)
    fact_text = _limit_text(fact_check, 5000)
    plan_text = _limit_text(plan, 3500)

    prompt = f"""
Create ONE section of an educational YouTube video.

VIDEO TOPIC:
{topic}

CONTENT PLAN:
{plan_text}

RESEARCH:
{research_text}

FACT CHECK:
{fact_text}

CURRENT SECTION:
{section_number} of {SECTION_COUNT}

SECTION TITLE:
{section_title}

Write approximately 120-170 spoken words for this section.

Requirements:

1. Write naturally for spoken YouTube narration.
2. Explain the subject clearly for a general audience.
3. Use only information supported by the research/fact-check context.
4. Do not invent statistics, studies, quotes, companies, dates,
   or other specific facts.
5. If something is uncertain, clearly describe it as uncertain.
6. Do not repeat the same information unnecessarily.
7. Do not use bullet points in the narration.
8. Do not write stage directions.
9. Do not write camera instructions.
10. Do not write "INTRO", "SCENE", or production notes.
11. Keep the language engaging but educational.

Return ONLY valid JSON:

{{
    "section_title": "{section_title}",
    "narration": "The complete spoken narration for this section."
}}
"""

    result = ask_ollama(
        prompt,
        system=(
            "You are an accurate educational YouTube script writer. "
            "Never present uncertain claims as established facts. "
            "Return valid JSON only."
        ),
        temperature=0.35,
    )

    if not isinstance(result, dict):
        raise RuntimeError(
            "Ollama returned an invalid section format."
        )

    narration = result.get("narration", "").strip()

    if not narration:
        raise RuntimeError(
            f"Section {section_number} returned empty narration."
        )

    return {
        "section_title": result.get(
            "section_title",
            section_title,
        ),
        "narration": narration,
    }


def write_script(topic, plan, research, fact_check):
    """
    Generate a complete YouTube script in several smaller sections.

    Returns:
        script_data, output_path
    """

    print()
    print("   Generating script in smaller sections...")
    print(
        f"   Target: approximately "
        f"{SECTION_COUNT} sections"
    )

    # Try to obtain useful section titles from the AI plan.
    suggested_sections = _get_field(
        plan,
        "suggested_sections",
        [],
    )

    if not isinstance(suggested_sections, list):
        suggested_sections = []

    # Default structure if the plan does not contain sections.
    default_sections = [
        "Introduction and the current state of AI",
        "How AI systems are changing work and everyday life",
        "Opportunities, limitations, and risks",
        "What the future of AI could look like",
    ]

    section_titles = []

    for title in suggested_sections:
        if isinstance(title, str) and title.strip():
            section_titles.append(title.strip())

    # Ensure exactly four useful sections.
    for title in default_sections:
        if len(section_titles) >= SECTION_COUNT:
            break

        if title not in section_titles:
            section_titles.append(title)

    section_titles = section_titles[:SECTION_COUNT]

    sections = []

    for index, title in enumerate(
        section_titles,
        start=1,
    ):

        print(
            f"   [{index}/{SECTION_COUNT}] "
            f"Writing: {title}"
        )

        section = _generate_section(
            topic=topic,
            plan=plan,
            research=research,
            fact_check=fact_check,
            section_number=index,
            section_title=title,
        )

        sections.append(section)

        print(
            f"   [{index}/{SECTION_COUNT}] "
            f"Section complete."
        )

    # Combine the sections into one narration.
    combined_parts = []

    for section in sections:
        combined_parts.append(
            section["narration"].strip()
        )

    full_script = "\n\n".join(combined_parts)

    # Approximate spoken duration.
    word_count = len(full_script.split())

    # Average educational narration speed.
    words_per_minute = 140

    estimated_minutes = (
        word_count / words_per_minute
    )

    script_data = {
        "title": topic,
        "hook": sections[0]["narration"],
        "script": full_script,
        "sections": sections,
        "chapters": [
            section["section_title"]
            for section in sections
        ],
        "word_count": word_count,
        "estimated_duration_minutes": round(
            estimated_minutes,
            2,
        ),
        "target_format": "YouTube educational video",
    }

    # Save the script.
    base_dir = Path(__file__).resolve().parent.parent

    output_dir = (
        base_dir
        / "data"
        / "scripts"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    output_path = (
        output_dir
        / f"script_{timestamp}.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            script_data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    print()
    print("   Script generation complete.")
    print(f"   Words: {word_count}")
    print(
        f"   Estimated duration: "
        f"{estimated_minutes:.2f} minutes"
    )
    print(f"   Saved: {output_path}")

    return script_data, output_path