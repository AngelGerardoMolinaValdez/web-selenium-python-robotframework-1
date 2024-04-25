import os
from jinja2 import Environment, FileSystemLoader
from test_report_library_context.reports.base_report import BaseReport

class HtmlSliderVerticalReport(BaseReport):
    def create(self, test_name, status, steps, setup_steps, teardown_steps, base_path):
        template_reports_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "assets", "static", 'templates'))
        report_dir = os.path.join(base_path, "html_vertical_slider")
        report_name = test_name + ".html"
        report_path = os.path.join(report_dir, report_name)

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        env = Environment(loader=FileSystemLoader(template_reports_path))
        template = env.get_template('step_vertical_slider_report.html')
        output = template.render(
            testname=test_name,
            steps_data=setup_steps+steps+teardown_steps,
            status=status
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(output)
