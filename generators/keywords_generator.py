import os
from typing import List
from keybert import KeyBERT
from data_models import StoryContent


class KeywordsGenerator:
	FIXED_KEYWORDS = [
		"ai", "openai", "image_generation", "dall-e-2",
		"text-davinci-003", "text_generation", "artificial intelligence",
		"story", "auto-generation", "kids"
	]

	def __init__(self, model: KeyBERT):
		self.model = model

	def generate_keywords(self, workdir: str, story_content: StoryContent) -> List[str]:
		"""
		Generate keywords from the given story
		:return: A list of keywords from the story
		"""
		keyword_data = self.model.extract_keywords(story_content.raw_text)
		keywords = self.FIXED_KEYWORDS + [keyword_entry[0] for keyword_entry in keyword_data]

		filename = os.path.join(workdir, f"keywords.txt")
		with open(filename, "w") as f:
			f.write(", ".join(keywords))

		return keywords
