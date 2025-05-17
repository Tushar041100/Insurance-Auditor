def check(file_number, text):
    findings = []
    if "insured person" in text.lower():
        findings.append({
            "file_number": file_number,
            "error_category": "Terminology",
            "description": "Non-standard term 'insured person' used.",
            "location": "-",
            "suggestion": "Use 'policyholder' instead"
        })
    return findings