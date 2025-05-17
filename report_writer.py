import pandas as pd

class ReportWriter:
    @staticmethod
    def write_report(findings, report_path):
        df = pd.DataFrame(findings, columns=[
            "file_number", "error_category", "description", "location", "suggestion"
        ])
        df.to_excel(report_path, index=False)