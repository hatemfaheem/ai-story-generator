import os
from typing import List
from keybert import KeyBERT
from data_models import StoryContent


class KeywordsGenerator:
    _FIXED_KEYWORDS = [
        "story",
        "kids",
    ]

    def __init__(self, model: KeyBERT):
        self.model = model

    def generate_keywords(self, workdir: str, story_content: StoryContent) -> List[str]:
        """Generate keywords from the given story
        Keywords can be used for Search Engine Optimization

        Args:
            workdir: The root workdir of the story
            story_content: The contents of the story

        Returns: A list of the most significant keywords in the story
        """
        keyword_data = self.model.extract_keywords(story_content.raw_text)
        keywords = self._FIXED_KEYWORDS + [
            keyword_entry[0] for keyword_entry in keyword_data
        ]

        filename = os.path.join(workdir, f"keywords.txt")
        with open(filename, "w") as f:
            f.write(", ".join(keywords))

        return keywords
