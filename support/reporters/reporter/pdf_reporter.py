from typing import Union
import base64
from io import BytesIO
from PIL import ImageGrab
from .base_reporter import BaseReporter

class PdfReporter(BaseReporter):
    def __init__(self, name: str, tags: Union[list, None]) -> None:
        super().__init__(name, tags)
        self.__buffered = BytesIO()
    
    def __take_screenshot(self) -> str:
        screenshot = ImageGrab.grab()
        self.__buffered.seek(0)
        screenshot.save(self.__buffered, format="JPEG", optimize=True)
        img_base64 = base64.b64encode(self.__buffered.getvalue()).decode('utf-8')
        return img_base64

    def add_content(self, desc: str, level: str):
        self._add_content(
            {
                "level": level,
                "message": desc,
                "image": self.__take_screenshot()
            }
        )
