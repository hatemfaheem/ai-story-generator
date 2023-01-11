import os
from gtts import gTTS
from data_models import StoryPageContent, AudioInfo
from generators.audio_generator_abstract import AbstractAudioGenerator


class AudioGeneratorGtts(AbstractAudioGenerator):
    def generate_audio(
        self, workdir: str, story_page_content: StoryPageContent
    ) -> AudioInfo:
        print(f"Generating audio for: {story_page_content.sentence}")
        audio = gTTS(text=story_page_content.sentence, lang="en", slow=True)
        mp3_filepath = self._get_mp3_filepath(workdir, story_page_content)
        audio.save(mp3_filepath)
        length_in_seconds = self._get_length_in_seconds(mp3_filepath)
        return AudioInfo(mp3_file=mp3_filepath, length_in_seconds=length_in_seconds)
