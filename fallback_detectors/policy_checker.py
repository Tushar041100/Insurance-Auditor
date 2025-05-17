import re

def check(file_number, text):
    findings = []
    for match in re.finditer(r"Policy No\.\s*(\d{10})", text):
        policy_no = match.group(1)
        if not policy_no.startswith("123"):
            findings.append({
                "file_number": file_number,
                "error_category": "Invalid Policy Number",
                "description": f"Policy number {policy_no} has an unexpected format.",
                "location": f"Offset {match.start(1)}",
                "suggestion": "Verify policy number"
            })
    return findings