"""Flashcard prompt templates."""

def get_flashcards_prompt(preset: str) -> str:
    """Get flashcards prompt for the specified preset."""

    base_flashcards = """
Create flashcards in JSON format from the following content for effective studying and retention.

Title: {title}
Source: {source}

Content:
{content}

Instructions:
- Generate 5-15 flashcards covering the most important concepts
- Each flashcard should have a clear question and comprehensive answer
- Focus on key facts, definitions, procedures, and relationships
- Make questions specific and answers complete but concise
- Use JSON format with "question" and "answer" fields

Format:
{{
  "flashcards": [
    {{
      "question": "What is...",
      "answer": "The answer explaining the concept clearly..."
    }}
  ]
}}
"""

    presets = {
        "general": base_flashcards,

        "runbook": base_flashcards + """
- Focus on operational procedures, troubleshooting steps, and decision trees
- Include "What should you do if..." scenarios
- Cover prerequisites, dependencies, and escalation procedures
- Include command examples and configuration details
""",

        "changelog": base_flashcards + """
- Focus on what changed and why it matters
- Include "What's new in version..." questions
- Cover breaking changes and migration steps
- Include "How do you upgrade..." procedural questions
"""
    }

    return presets.get(preset, base_flashcards)
