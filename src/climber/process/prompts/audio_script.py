"""Audio script prompt templates."""

def get_audio_script_prompt(preset: str) -> str:
    """Get audio script prompt for the specified preset."""

    base_audio_script = """
Create an engaging audio script for Text-to-Speech that teaches the following content in a conversational, educational style.

Title: {title}
Source: {source}

Content:
{content}

Instructions:
- Write in a conversational, teaching tone as if explaining to a colleague
- Use natural speech patterns with appropriate pauses and transitions
- Break complex concepts into digestible explanations
- Include analogies and examples where helpful
- Structure with clear sections and smooth transitions
- Aim for 5-10 minute listening time
- Use "Let's talk about...", "Now, here's something interesting...", etc.
- Don't just read the content - teach and explain it

Format as a structured script with clear sections and natural flow.
"""

    presets = {
        "general": base_audio_script,

        "runbook": base_audio_script + """
- Focus on step-by-step procedures and operational guidance
- Use "First, you'll want to...", "Next, make sure to...", "If this happens..."
- Explain the reasoning behind each step
- Include troubleshooting tips and common pitfalls
- Make it sound like experienced colleague training
""",

        "changelog": base_audio_script + """
- Structure as "What's changed and why you should care"
- Use "The big news is...", "This affects you if...", "Here's what you need to know..."
- Explain the context and impact of changes
- Include upgrade recommendations and timeline considerations
"""
    }

    return presets.get(preset, base_audio_script)
