from typing import Union
import os
import uuid
from PIL import ImageGrab
from .base_reporter import BaseReporter

class PdfReporter(BaseReporter):
    image_output_path = None

    @classmethod
    def get_image_output_path(cls):
        cls.set_image_output_directory()
        return cls.image_output_path

    @classmethod
    def set_image_output_directory(cls):
        if cls.image_output_path is None:
            cls.image_output_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "..", "..", "..", "output", "images")
            )

    def __new__(cls, *args, **kwargs):
        cls.set_image_output_directory()
        return super().__new__(cls)

    def __init__(self, name: str, tags: Union[list, None]) -> None:
        super().__init__(name, tags)
    
    def __take_screenshot(self) -> str:
        image_path = os.path.join(self.image_output_path, str(uuid.uuid4()) + ".jpg")
        screenshot = ImageGrab.grab()
        screenshot.save(image_path, format="JPEG", optimize=True)
        return image_path

    def add_content(self, desc: str, level: str):
        self._add_content(
            {
                "level": level,
                "message": desc,
                "image": self.__take_screenshot()
            }
        )
