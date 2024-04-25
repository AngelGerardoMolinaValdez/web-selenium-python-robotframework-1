from enum import Enum
from test_report_library_context.reports.html_slider_horizontal_report import HtmlSliderHorizontalReport
from test_report_library_context.reports.html_slider_vertical_report import HtmlSliderVerticalReport
from test_report_library_context.reports.pdf_slider_report import PdfSliderReport

class ReportTypes(Enum):
    PDF_SLIDER = PdfSliderReport
    HTML_VERTICAL_SLIDER = HtmlSliderVerticalReport
    HTML_HORIZONTAL_SLIDER = HtmlSliderHorizontalReport
