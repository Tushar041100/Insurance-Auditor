import language_tool_python
import time
from language_tool_python.utils import RateLimitError

def check_typos_in_chunks(text, tool, chunk_size=5000, max_retries=3):
    """
    Splits the text into smaller chunks and checks each chunk for typos.
    Implements retry logic with exponential backoff for rate limit errors.
    """
    matches = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        retries = 0
        while retries < max_retries:
            try:
                matches.extend(tool.check(chunk))
                break  # Exit retry loop on success
            except RateLimitError:
                retries += 1
                if retries < max_retries:
                    delay = 2 ** retries  # Exponential backoff
                    time.sleep(delay)
                else:
                    raise RateLimitError("Max retries exceeded for LanguageTool API.")
    return matches

def check(file_number, text):
    tool = language_tool_python.LanguageToolPublicAPI('en-US')
    matches = check_typos_in_chunks(text, tool)
    findings = []
    for match in matches:
        description = match.message
        location = f"Positions {match.offset}-{match.offset+match.errorLength}"
        suggestion = "; ".join(match.replacements)
        findings.append({
            "file_number": file_number,
            "error_category": "Spelling/Grammar",
            "description": description,
            "location": location,
            "suggestion": suggestion or "Check spelling/grammar"
        })
    return findings
