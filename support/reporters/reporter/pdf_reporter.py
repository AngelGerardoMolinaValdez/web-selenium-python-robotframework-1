import base64
from io import BytesIO
from PIL import ImageGrab
from .base_reporter import BaseReporter

class PdfReporter(BaseReporter):
    def __init__(self, output_dir: str, name: str) -> None:
        super().__init__(output_dir, name)
    
    def __take_screenshot(self) -> str:
        screenshot = ImageGrab.grab()
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def add_content_to_report(self, desc: str, level: str):
        self._add_data(
            {
                "level": level,
                "message": desc,
                "image": self.__take_screenshot()
            }
        )
