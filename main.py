import argparse
from typing import Optional

from keybert import KeyBERT
from generators.audio_generator import AudioGenerator
from generators.image_generator import ImageGenerator
from generators.keywords_generator import KeywordsGenerator
from generators.story_content_generator import StoryContentGenerator
from generators.text_generator import TextGenerator
from processors.page_processor import PageProcessor
from processors.pdf_processor import PdfProcessor
from processors.text_processor import TextProcessor
from processors.video_processor import VideoProcessor
from story_manager import StoryManager
from story_provider import StoryProvider
from util.openai_credentials_provider import OpenAICredentialsProvider
from util.story_utility import StoryUtility


def create_story_provider(openai_creds_json_filepath: str) -> StoryProvider:
    """A factory-like method for the story provider."""
    story_utility = StoryUtility()
    text_processor = TextProcessor()
    text_generator = TextGenerator(text_processor=text_processor)
    image_generator = ImageGenerator()
    credentials_provider = OpenAICredentialsProvider(json_filepath=openai_creds_json_filepath)
    story_content_generator = StoryContentGenerator(text_generator=text_generator,
                                                    image_generator=image_generator,
                                                    credentials_provider=credentials_provider)
    return StoryProvider(story_utility=story_utility, story_content_generator=story_content_generator)


def create_story_manager() -> StoryManager:
    """A factory-like method for the story manager."""
    audio_generator = AudioGenerator()
    keybert_model = KeyBERT()
    keywords_generator = KeywordsGenerator(model=keybert_model)
    page_processor = PageProcessor()
    pdf_processor = PdfProcessor()
    video_processor = VideoProcessor()

    return StoryManager(
        audio_generator=audio_generator,
        keywords_generator=keywords_generator,
        page_processor=page_processor,
        pdf_processor=pdf_processor,
        video_processor=video_processor
    )


def enact(story_prompt: Optional[str], pickle_file: Optional[str], openai_creds_json_filepath: str):
    story_provider: StoryProvider = create_story_provider(openai_creds_json_filepath=openai_creds_json_filepath)
    story_manager: StoryManager = create_story_manager()
    combined_workdir, story_content = story_provider.generate_or_load(story_prompt=story_prompt, pickle_file=pickle_file)
    story_manager.invoke(combined_workdir=combined_workdir, story_content=story_content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--openai-creds", help="Credentials file in json format for Open AI org and api_key.",
                        default="openai_creds.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--prompt", help="The title/prompt of the story to be generated e.g. the colorful butterfly")
    group.add_argument("--pickle", help="A pickle file to load an existing story. "
                                        "For example: ./_stories/2023_01_06_17_38_47"
                                        "-Five_Little_Monkeys/story_content.pickle")
    args = parser.parse_args()
    enact(story_prompt=args.prompt, pickle_file=args.pickle, openai_creds_json_filepath=args.openai_creds)
