import openai

from data_models import StoryText
from processors.text_processor import TextProcessor


class TextGenerator:
    def __init__(self, text_processor: TextProcessor):
        self.text_processor = text_processor

    def generate_story_text(self, prompt: str) -> StoryText:
        """
        Generate story text, given prompt.
        :param prompt: The title/seed of the story, e.g. "The Brave Dog"
        :return: raw_text and processed_text (sentences)
        """
        story_content = openai.Completion.create(
            model="text-davinci-003",
            prompt="Give me a story about " + prompt,
            max_tokens=256,
            temperature=0
        )
        story_raw_text = story_content["choices"][0]["text"]
        processed_sentences = self.text_processor.process_story_text(story_raw_text=story_raw_text)
        print(f"Raw story text: {story_raw_text}")
        return StoryText(raw_text=story_raw_text, processed_sentences=processed_sentences)
