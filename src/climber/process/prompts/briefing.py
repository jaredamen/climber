"""Briefing prompt templates."""


def get_briefing_prompt(preset: str) -> str:
    """Get briefing prompt for the specified preset."""

    base_briefing = """
Create a 2-minute executive briefing from the following content.

Title: {title}
Source: {source}

Content:
{content}

Instructions:
- Write a concise executive summary that can be read in 2 minutes
- Focus on the most important key points and takeaways
- Use clear, professional language
- Structure with bullet points or short paragraphs
- Assume the reader is knowledgeable but busy
"""

    presets = {
        "general": base_briefing,
        "runbook": base_briefing
        + """
- Focus on operational procedures, decision points, and critical steps
- Highlight prerequisites, dependencies, and potential failure modes
- Include escalation paths and key contacts if mentioned
- Emphasize actionable information
""",
        "changelog": base_briefing
        + """
- Focus on what changed, what's new, and what affects users
- Categorize changes by impact level (breaking, feature, fix, etc.)
- Highlight migration steps or action items for users
- Include version numbers and dates if available
""",
    }

    return presets.get(preset, base_briefing)
