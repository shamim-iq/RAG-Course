"""Markdown runbook -> text with headings and command blocks preserved."""


def load_md(file_path):
    """Markdown is already text; no Markdown renderer is required."""
    # Keep headings and commands because they provide troubleshooting context.
    # You should understand ----------------------------------------------------->
    text = file_path.read_text(encoding="utf-8")
    return text
    # -------------------------------------------------------------------------->
