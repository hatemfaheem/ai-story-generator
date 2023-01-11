from data_models import StoryPageContent, AudioInfo
from generators.audio_generator_abstract import AbstractAudioGenerator

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing

from util.aws_polly_credentials_provider import AwsPollyCredentialsProvider


class AudioGeneratorPolly(AbstractAudioGenerator):
    _ENGINE_NEUTRAL: str = "neural"
    _VOICE_ID: str = "Kevin"
    _OUTPUT_FORMAT_MP3: str = "mp3"
    _LANGUAGE_CODE_EN_US: str = "en-US"
    _SPEED: str = "x-slow"
    _TEXT_TYPE_SSML: str = "ssml"

    def __init__(self, aws_polly_credentials_provider: AwsPollyCredentialsProvider):
        self.session = Session(
            aws_access_key_id=aws_polly_credentials_provider.access_key,
            aws_secret_access_key=aws_polly_credentials_provider.secret_key,
        )
        self.polly = self.session.client("polly")

    def generate_audio(
        self, workdir: str, story_page_content: StoryPageContent
    ) -> AudioInfo:
        print(f"Generating audio for: {story_page_content.sentence}")
        response = self._call_polly(story_page_content.sentence)

        # Access the audio stream from the response
        if response and "AudioStream" in response:
            mp3_filepath = self._handle_polly_response(
                workdir, story_page_content, response
            )
            length_in_seconds = self._get_length_in_seconds(mp3_filepath)
            return AudioInfo(mp3_filepath, length_in_seconds)
        else:
            # The response didn't contain audio data, exit gracefully
            raise RuntimeError(
                f"Error performing text to speech using Polly, could not stream audio"
            )

    def _call_polly(self, text: str):
        try:
            # Request speech synthesis
            return self.polly.synthesize_speech(
                Engine=self._ENGINE_NEUTRAL,
                TextType=self._TEXT_TYPE_SSML,
                Text=self._construct_ssml(text=text),
                OutputFormat=self._OUTPUT_FORMAT_MP3,
                VoiceId=self._VOICE_ID,
                LanguageCode=self._LANGUAGE_CODE_EN_US,
            )
        except (BotoCoreError, ClientError) as error:
            print(f"Error performing text to speech using Polly: {error}")
            return None

    def _handle_polly_response(
        self, workdir: str, story_page_content: StoryPageContent, response
    ) -> str:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
        with closing(response["AudioStream"]) as stream:
            mp3_filepath = self._get_mp3_filepath(workdir, story_page_content)
            try:
                # Open a file for writing the output as a binary stream
                with open(mp3_filepath, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(
                    f"Error performing text to speech using Polly, could not write to file: {error}"
                )

        return mp3_filepath

    def _construct_ssml(self, text: str):
        return f'<speak><prosody rate="{self._SPEED}">{text}.</prosody></speak>'
