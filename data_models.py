from dataclasses import dataclass
from enum import Enum
from typing import List

from PIL.Image import Image


class StorySize(Enum):
    """The sizing configuration of the story."""

    SIZE_256 = (256, 455)
    SIZE_512 = (512, 910)
    SIZE_1024 = (1024, 1820)

    def __init__(self, image_part_size: int, page_width: int):
        self.page_width: int = page_width
        self.page_height: int = image_part_size
        self.image_part_size: str = f"{image_part_size}x{image_part_size}"
        self.text_part_width: int = page_width - image_part_size
        self.text_part_height: int = image_part_size
        self.font_size: int = self._get_font_size(image_part_size)

    @staticmethod
    def get_size_from_str(size: str):
        return {
            "256": StorySize.SIZE_256,
            "512": StorySize.SIZE_512,
            "1024": StorySize.SIZE_1024,
        }[size]

    @staticmethod
    def _get_font_size(size: int) -> int:
        return {256: 16, 512: 38, 1024: 58}[size]


@dataclass
class StoryPageContent:
    sentence: str
    image: Image
    image_path: str
    page_number: str


@dataclass
class StoryText:
    raw_text: str
    processed_sentences: List[str]


@dataclass
class StoryContent:
    story_seed: str
    raw_text: str
    page_contents: List[StoryPageContent]
    story_size: StorySize


@dataclass
class AudioInfo:
    mp3_file: str
    length_in_seconds: float


@dataclass
class StoryPage:
    page_content: StoryPageContent
    page_image: Image
    page_filepath: str
    audio: AudioInfo


@dataclass
class Story:
    story_seed: str
    story_raw_text: str
    pages: List[StoryPage]
    start_page_filepath: str
    end_page_filepath: str
    keywords: List[str]


@dataclass
class CombinedWorkdir:
    workdir: str
    workdir_images: str
    workdir_pages: str
    workdir_audio: str
