import os
from gtts import gTTS
from mutagen.mp3 import MP3
from data_models import StoryPageContent, AudioInfo


class AudioGenerator:
    def generate_audio(
        self, workdir: str, story_page_content: StoryPageContent
    ) -> AudioInfo:
        """Preform text to speech and generate an audio file for the given story page

        Args:
            workdir: The workdir where to save the audio files
            story_page_content: The content of a single page from the story

        Returns: A local file path for the generated audio file
        """

        print(f"Generating audio for: {story_page_content.sentence}")
        audio = gTTS(text=story_page_content.sentence, lang="en", slow=True)
        mp3_filepath = os.path.join(
            workdir, f"audio_{story_page_content.page_number}.mp3"
        )
        audio.save(mp3_filepath)
        length_in_seconds = self._get_length_in_seconds(mp3_filepath)
        return AudioInfo(mp3_file=mp3_filepath, length_in_seconds=length_in_seconds)

    @staticmethod
    def _get_length_in_seconds(mp3_filepath: str) -> float:
        return MP3(mp3_filepath).info.length
