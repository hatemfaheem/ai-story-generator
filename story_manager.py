from typing import List

from data_models import Story, StoryPage, StoryContent, CombinedWorkdir, StorySize
from generators.audio_generator_abstract import AbstractAudioGenerator
from generators.keywords_generator import KeywordsGenerator
from processors.page_processor import PageProcessor
from processors.pdf_processor import PdfProcessor
from processors.video_processor import VideoProcessor


class StoryManager:
    """
    Given Story Content (Image and Text), this class will:
     1. Generate audio.
     2. Create pages.
     3. Generate video.
     4. Generate keywords.
     5. Create PDF.
    """

    def __init__(
        self,
        audio_generator: AbstractAudioGenerator,
        keywords_generator: KeywordsGenerator,
        page_processor: PageProcessor,
        pdf_processor: PdfProcessor,
        video_processor: VideoProcessor,
    ):
        self.audio_generator = audio_generator
        self.keywords_generator = keywords_generator
        self.page_processor = page_processor
        self.pdf_processor = pdf_processor
        self.video_processor = video_processor

    def invoke(self, combined_workdir: CombinedWorkdir, story_content: StoryContent):
        story_pages: List[StoryPage] = []
        for page_content in story_content.page_contents:
            audio = self.audio_generator.generate_audio(
                workdir=combined_workdir.workdir_audio, story_page_content=page_content
            )
            page: StoryPage = self.page_processor.create_page(
                workdir=combined_workdir.workdir_pages,
                story_page_content=page_content,
                audio=audio,
                story_size=story_content.story_size,
            )
            story_pages.append(page)

        start_page_filepath = self.page_processor.create_start_page(
            workdir=combined_workdir.workdir_pages,
            prompt=story_content.story_seed,
            story_size=story_content.story_size,
        )
        end_page_filepath = self.page_processor.create_end_page(
            workdir=combined_workdir.workdir_pages, story_size=story_content.story_size
        )
        keywords = self.keywords_generator.generate_keywords(
            workdir=combined_workdir.workdir, story_content=story_content
        )

        story = Story(
            story_seed=story_content.story_seed,
            story_raw_text=story_content.raw_text,
            pages=story_pages,
            start_page_filepath=start_page_filepath,
            end_page_filepath=end_page_filepath,
            keywords=keywords,
        )

        self.pdf_processor.create_pdf(workdir=combined_workdir.workdir, story=story)
        self.video_processor.generate_video(
            workdir=combined_workdir.workdir, story=story
        )
