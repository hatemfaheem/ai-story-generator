from dataclasses import dataclass
from typing import List

from PIL import Image


class StoryPageContent:
    def __init__(self, sentence: str, image: Image, image_path: str, number: str):
        self.sentence: str = sentence
        self.image: Image = image
        self.image_path: str = image_path
        self.page_number: str = number


@dataclass
class StoryText:
    raw_text: str
    processed_sentences: List[str]


@dataclass
class StoryContent:
    story_seed: str
    raw_text: str
    page_contents: List[StoryPageContent]


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
