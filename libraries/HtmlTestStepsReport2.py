import os
import re
import datetime
from jinja2 import Environment, FileSystemLoader

class HtmlTestStepsReport2:
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.keyword_config = bool
        self.keywords_config = []
        self.keywords_data = []
        self.current_test = {}
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        if not os.path.exists(os.path.join(self.base_path, "output")):
            os.mkdir(os.path.join(self.base_path, "output"))

        if not os.path.exists(os.path.join(self.base_path, "output", "reports")):
            os.mkdir(os.path.join(self.base_path, "output", "reports"))

        if not os.path.exists(os.path.join(self.base_path, "output", "robot")):
            os.mkdir(os.path.join(self.base_path, "output", "robot"))

    def start_test(self, name, attrs):
        self.current_test = {
            'name': name
        }

    def end_test(self, name, attrs):
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path_to_report = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output", "reports", self.current_test["name"] + " " + today.replace(":", "-")))

        os.mkdir(path_to_report)
        env = Environment(loader=FileSystemLoader(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "static", 'templates'))
            )
        )
        template = env.get_template('step_report_2.html')
        output = template.render(testname=self.current_test["name"], steps_data=self.keywords_config + self.keywords_data)
        with open(os.path.join(path_to_report, self.current_test["name"] + ".html"), "w", encoding="utf-8") as f:
            f.write(output)

        self.keywords_data = []

    def start_keyword(self, name, attrs):
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = True

    def end_keyword(self, name, attrs):
        tag_message_title = re.search(r"STEP:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FALTA|WARNING|DEBUG))?(?:===|:|$)", "===>".join(attrs['tags']))

        if tag_message_title:
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title

            if self.keyword_config:
                self.keywords_config.append(step_data)
            else:
                self.keywords_data.append(step_data)
        
        if attrs['type'].lower() in ['setup', 'teardown']:
            self.keyword_config = False

    def log_message(self, message):
        tag_message_title = re.search(r"STEP:(.+?)(?::(INFO|PASS|CRITICAL|FAIL|FALTA|WARNING|DEBUG))?(?:===|:|$)", message['message'])

        if tag_message_title:
            step_data = {}
            level = tag_message_title.group(2) if tag_message_title.group(2) else "INFO"
            step_title = tag_message_title.group(1)
            step_data["step_level"] = level.lower()
            step_data["step_title"] = step_title

            self.keywords_data.append(step_data)
