import os
from abc import ABC, abstractmethod

from mutagen.mp3 import MP3

from data_models import AudioInfo, StoryPageContent


class AbstractAudioGenerator(ABC):
    @abstractmethod
    def generate_audio(
        self, workdir: str, story_page_content: StoryPageContent
    ) -> AudioInfo:
        """Preform text to speech and generate an audio file for the given story page

        Args:
            workdir: The workdir where to save the audio files
            story_page_content: The content of a single page from the story

        Returns: AudioInfo object with filepath and length.
        """
        pass

    @staticmethod
    def _get_length_in_seconds(mp3_filepath: str) -> float:
        return MP3(mp3_filepath).info.length

    @staticmethod
    def _get_mp3_filepath(workdir: str, story_page_content: StoryPageContent) -> str:
        return os.path.join(workdir, f"audio_{story_page_content.page_number}.mp3")
