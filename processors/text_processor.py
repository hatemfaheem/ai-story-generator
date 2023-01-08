from typing import List

import nltk


class TextProcessor:
    def process_story_text(self, story_raw_text: str) -> List[str]:
        story_sentences = nltk.sent_tokenize(story_raw_text)
        return [self._clean_text(sentence) for sentence in story_sentences if sentence]

    @staticmethod
    def _clean_text(text: str) -> str:
        return text.strip().replace("\n", "")
