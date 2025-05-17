import re

def check(file_number, text):
    findings = []
    for match in re.finditer(r"\$([\d,]+)", text):
        amount = int(match.group(1).replace(",", ""))
        if amount > 10000000:
            findings.append({
                "file_number": file_number,
                "error_category": "Unrealistic Coverage",
                "description": f"Coverage amount ${amount} seems too high.",
                "location": f"Offset {match.start(1)}",
                "suggestion": "Confirm with underwriting policy"
            })
    return findings