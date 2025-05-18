# Insurance-Auditor

Insurance-Auditor is a document analysis tool designed to audit insurance-related documents for errors such as spelling/grammar issues, invalid policy numbers, unrealistic coverage amounts, and incorrect terminology. It uses a combination of a language model (LLM) and fallback detectors to ensure comprehensive analysis.

## Features

- Document Analysis: Supports PDF, DOCX, XLSX, and TXT file formats.
- Error Detection:
  - Spelling and grammar issues.
  - Invalid policy numbers.
  - Unrealistic coverage amounts.
  - Non-standard terminology.
- Fallback Mechanism: Uses custom detectors when the LLM is unavailable or rate-limited.
- Report Generation: Outputs findings in an Excel report.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Insurance-Auditor.git
   cd Insurance-Auditor

2. Install dependencies:
   pip install -r requirements.txt

3. Set up environment variables:
   - Create a .env file in the root directory.
   - Add your GROQ_API_KEY:
    GROQ_API_KEY=your_api_key_here

## Usage

1. Run the application:
   streamlit run main.py

2. Upload documents via the web interface.

3. Analyze the documents and download the generated Excel report.

## Project Structure
Insurance-Auditor/\
├── fallback_detectors/       # Custom fallback detectors for error analysis\
│   ├── coverage_checker.py   # Detects unrealistic coverage amounts\
│   ├── policy_checker.py     # Validates policy numbers\
│   ├── spelling_grammar.py   # Checks spelling and grammar\
│   ├── terminology_checker.py # Detects non-standard terminology\
├── utils/                    # Utility functions\
│   ├── file_extractors.py    # Extracts text from various file formats\
├── llm_engine.py             # Core logic for LLM-based analysis\
├── main.py                   # Streamlit-based user interface\
├── report_writer.py          # Generates Excel reports\
├── requirements.txt          # Python dependencies\
├── .gitignore                # Git ignore rules\
├── LICENSE                   # License information\
└── README.md                 # Project documentation\

## Dependencies
- streamlit: For the web interface.
- groq: For interacting with the LLM.
- pandas: For data manipulation and report generation.
- openpyxl: For writing Excel reports.
- python-docx: For extracting text from DOCX files.
- PyPDF2: For extracting text from PDF files.
- language-tool-python: For spelling and grammar checks.
- dotenv: For managing environment variables.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- LanguageTool for spelling and grammar checks.
- Streamlit for the user interface.
- Groq for LLM integration.