import os
from gtts import gTTS
from mutagen.mp3 import MP3
from data_models import StoryPageContent, AudioInfo


class AudioGenerator:
    @staticmethod
    def generate_audio(workdir: str, story_page_content: StoryPageContent) -> AudioInfo:
        """
        Preform text to speech and generate an audio file for the given story page
        :param workdir: the workdir where to save the audio files
        :param story_page_content: The content of a single page from the story
        :return: A local file path for the generated audio file
        """
        print(f"Generating audio for: {story_page_content.sentence}")
        audio = gTTS(text=story_page_content.sentence, lang="en", slow=True)
        mp3_file = os.path.join(workdir, f"audio_{story_page_content.page_number}.mp3")
        audio.save(mp3_file)
        length_in_seconds = MP3(mp3_file).info.length
        return AudioInfo(mp3_file=mp3_file, length_in_seconds=length_in_seconds)
