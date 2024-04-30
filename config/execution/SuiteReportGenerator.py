import os
from jinja2 import Environment, FileSystemLoader

class SuiteReportGenerator:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self) -> None:
        self.__tests_info = []
        self.__counter_pass_tests = 0
        self.__counter_fail_tests = 0
        self.__counter_skip_tests = 0

    def end_test(self, name, attrs):
        self.__tests_info.append({
            "id": attrs['id'],
            'name': attrs['longname'],
            'status': attrs['status'],
            'message': attrs['message']
        })
        if attrs['status'] == 'PASS':
            self.__counter_pass_tests += 1
        elif attrs['status'] == 'FAIL':
            self.__counter_fail_tests += 1
        elif attrs['status'] == 'SKIP':
            self.__counter_skip_tests += 1

    def close(self):
        base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'output', 'reports')
        template_reports_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "assets", "static", 'templates'))
        report_dir = os.path.join(base_path, "suite_report")
        report_name = "suite_report" + ".html"
        report_path = os.path.join(report_dir, report_name)

        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        env = Environment(loader=FileSystemLoader(template_reports_path))
        template = env.get_template('suite_report.html')
        output = template.render(
            tests_info=self.__tests_info,
            counter_pass_tests=self.__counter_pass_tests,
            counter_fail_tests=self.__counter_fail_tests,
            counter_skip_tests=self.__counter_skip_tests,
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(output)
