# === Updated llm_engine.py with retry ===
import os, json, logging, textwrap, time, re
from groq import Groq
from utils.file_extractors import extract_text_from_file
from fallback_detectors import spelling_grammar, policy_checker, coverage_checker, terminology_checker
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def analyze_document(file_name, file_bytes):
    file_number = os.path.splitext(file_name)[0]
    text = extract_text_from_file(file_name, file_bytes)

    chunks = split_text_into_chunks(text, max_chars=4000)
    all_findings = []
    for idx, chunk in enumerate(chunks):
        prompt = construct_prompt(file_number, chunk)
        attempt = 0
        while attempt < 2:
            try:
                response = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.3-70b-versatile"
                )
                content = response.choices[0].message.content
                print (content)
                findings = json.loads(content)
                all_findings.extend(findings)
                break  # exit retry loop on success
            except Exception as e:
                error_str = str(e)
                logger.error(f"LLM analysis failed for chunk {idx + 1} of {file_number}: {error_str}")
                wait_time = extract_wait_time_seconds(error_str)
                if wait_time:
                    logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time + 1)
                    attempt += 1
                else:
                    fallback_findings = run_fallback_detectors(file_number, chunk)
                    all_findings.extend(fallback_findings)
                    break

    return all_findings

def construct_prompt(file_number, text):
    instructions = textwrap.dedent(f"""
        You are an insurance title document auditor. Analyze the following document (ID {file_number}) and identify errors:
        1. Spelling/grammar
        2. Missing information
        3. Name/date inconsistencies
        4. Invalid policy numbers
        5. Unrealistic coverage amounts
        6. Incorrect terminology

        Return a JSON array with keys:
        - file_number
        - error_category
        - description
        - location
        - suggestion
    """)
    return instructions + "\n\nDocument Content:\n" + text

def run_fallback_detectors(file_number, text):
    findings = []
    findings += spelling_grammar.check(file_number, text)
    findings += policy_checker.check(file_number, text)
    findings += coverage_checker.check(file_number, text)
    findings += terminology_checker.check(file_number, text)
    return findings

def split_text_into_chunks(text, max_chars=4000, overlap=200):
    words = text.split()
    chunks = []
    current = []
    total_chars = 0

    for word in words:
        if total_chars + len(word) + 1 > max_chars:
            chunks.append(" ".join(current))
            current = current[-(overlap // 5):]  # retain overlap
            total_chars = sum(len(w) for w in current)
        current.append(word)
        total_chars += len(word) + 1

    if current:
        chunks.append(" ".join(current))
    return chunks

def extract_wait_time_seconds(message):
    try:
        match = re.search(r'try again in (\d+(?:\.\d+)?)s', message)
        if match:
            return float(match.group(1))
    except Exception:
        pass
    return None
