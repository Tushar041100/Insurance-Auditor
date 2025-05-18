import streamlit as st
import os
from llm_engine import analyze_document
from report_writer import ReportWriter

def main():
    st.title("Stewart Title Insurance Document Analyzer")
    uploaded_files = st.file_uploader(
        "Upload documents (PDF, DOCX, XLSX, TXT)",
        type=["pdf", "docx", "xlsx", "txt"],
        accept_multiple_files=True
    )
    if st.button("Analyze Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
            return
        all_findings = []
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name
            file_bytes = uploaded_file.read()
            try:
                findings = analyze_document(file_name, file_bytes)
                all_findings.extend(findings)
                st.success(f"Analysis complete for {file_name}.")
            except Exception as e:
                st.error(f"Failed to analyze {file_name}: {e}")
        if all_findings:
            report_path = os.path.join(os.getcwd(), "error_report.xlsx")
            ReportWriter.write_report(all_findings, report_path)
            st.success(f"Analysis report saved: {report_path} and you can download the report:")
        
        with open(report_path, "rb") as f:
            st.download_button("Download Excel Report", data=f, file_name="error_report.xlsx")

if __name__ == "__main__":
    main()