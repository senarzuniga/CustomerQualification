import io
from datetime import datetime

try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ImportError:
    FPDF_AVAILABLE = False


class PDFReportGenerator:
    def generate_report(self, company_name: str, all_analysis: dict, report_text: str) -> bytes:
        if not FPDF_AVAILABLE:
            return self._text_fallback(company_name, report_text)
        try:
            return self._build_pdf(company_name, all_analysis, report_text)
        except Exception:
            return self._text_fallback(company_name, report_text)

    def _build_pdf(self, company_name: str, all_analysis: dict, report_text: str) -> bytes:
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Cover page
        pdf.add_page()
        pdf.set_fill_color(31, 119, 180)
        pdf.rect(0, 0, 210, 297, "F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 28)
        pdf.set_xy(20, 80)
        safe_name = company_name.encode("latin-1", errors="replace").decode("latin-1")
        pdf.cell(170, 15, safe_name, align="C")
        pdf.set_font("Helvetica", "", 16)
        pdf.set_xy(20, 105)
        pdf.cell(170, 10, "Informe de Inteligencia Empresarial", align="C")
        pdf.set_font("Helvetica", "", 12)
        pdf.set_xy(20, 125)
        pdf.cell(170, 8, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}", align="C")

        val = all_analysis.get("valuation", {}).get("valuation", {})
        if val.get("estimated_value_m"):
            pdf.set_xy(20, 145)
            pdf.cell(170, 8, f"Valoracion estimada: {val['estimated_value_m']} M EUR", align="C")

        sale = all_analysis.get("valuation", {}).get("sale_propensity", {})
        if sale.get("recommendation"):
            pdf.set_xy(20, 160)
            rec = sale["recommendation"].encode("latin-1", errors="replace").decode("latin-1")
            pdf.cell(170, 8, f"Recomendacion: {rec}", align="C")

        # Content pages
        pdf.set_text_color(0, 0, 0)
        pdf.add_page()
        pdf.set_fill_color(255, 255, 255)

        lines = report_text.split("\n")
        for line in lines:
            safe_line = line.encode("latin-1", errors="replace").decode("latin-1")
            if safe_line.startswith("# "):
                pdf.set_font("Helvetica", "B", 16)
                pdf.set_text_color(31, 119, 180)
                pdf.multi_cell(0, 10, safe_line[2:])
                pdf.set_text_color(0, 0, 0)
            elif safe_line.startswith("## "):
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(31, 119, 180)
                pdf.ln(3)
                pdf.multi_cell(0, 8, safe_line[3:])
                pdf.set_text_color(0, 0, 0)
            elif safe_line.startswith("### "):
                pdf.set_font("Helvetica", "B", 11)
                pdf.multi_cell(0, 7, safe_line[4:])
            elif safe_line.startswith("**") and safe_line.endswith("**"):
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(0, 6, safe_line.strip("*"))
            elif safe_line.startswith("- ") or safe_line.startswith("* "):
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, "  " + safe_line[2:])
            elif safe_line.strip() == "":
                pdf.ln(2)
            else:
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 6, safe_line)

        # Footer on each page
        pdf.set_y(-15)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(128, 128, 128)
        pdf.cell(0, 10, f"Pagina {pdf.page_no()} | {safe_name} | {datetime.now().strftime('%d/%m/%Y')}", align="C")

        buf = io.BytesIO()
        pdf.output(buf)
        return buf.getvalue()

    def _text_fallback(self, company_name: str, report_text: str) -> bytes:
        return report_text.encode("utf-8")
