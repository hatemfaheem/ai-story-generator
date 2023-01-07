import openai

from data_models import StoryPageContent, StoryContent
from generators.image_generator import ImageGenerator
from generators.text_generator import TextGenerator
from util.openai_credentials_provider import OpenAICredentialsProvider


class StoryContentGenerator:
	def __init__(self, text_generator: TextGenerator, image_generator: ImageGenerator, credentials_provider: OpenAICredentialsProvider):
		openai.organization = credentials_provider.organization
		openai.api_key = credentials_provider.api_key
		self.image_generator = image_generator
		self.text_generator = text_generator

	def generate_new_story(self, workdir_images: str, story_seed_prompt: str) -> StoryContent:
		"""
		Generate a new story for the given prompt
		:param workdir_images: workdir to save generated images
		:param story_seed_prompt: The title/seed of the story, e.g. "The Brave Dog"
		:return: The contents of the story.
		"""
		story_text = self.text_generator.generate_story_text(story_seed_prompt)
		raw_text = story_text.raw_text
		processed_sentences = story_text.processed_sentences
		page_contents = []

		for i in range(len(processed_sentences)):
			image_prompt = f"Generate art for {story_seed_prompt} {processed_sentences[i]} as a children's book illustration"
			url = self.image_generator.generate_image(prompt=image_prompt)
			image_number: str = str(i).zfill(3)
			image, image_path = self.image_generator.download_image(
				workdir=workdir_images, url=url, prompt=processed_sentences[i], image_number=image_number)
			story_page_content = StoryPageContent(
				sentence=processed_sentences[i],
				image=image,
				image_path=image_path,
				page_number=image_number)
			page_contents.append(story_page_content)

		return StoryContent(story_seed=story_seed_prompt, raw_text=raw_text, page_contents=page_contents)
