import os
from io import BytesIO
from typing import Tuple

import openai
import requests
from PIL import Image


class ImageGenerator:
    _IMAGE_SIZE: str = "256x256"

    def generate_image(self, prompt: str) -> str:
        """Generate an image for the given prompt/sentence

        Args:
            prompt: the text to generate an image for

        Returns: The url for the generated image
        """
        response = openai.Image.create(prompt=prompt, n=1, size=self._IMAGE_SIZE)
        url = response["data"][0]["url"]
        print(f"Generated image for prompt '{prompt}': {url}")
        return url

    @staticmethod
    def download_image(
        workdir: str, url: str, image_number: str
    ) -> Tuple[Image.Image, str]:
        """Download the image from the given url

        Args:
            workdir: The workdir where to download the image
            url: The url of the image to download
            image_number: The number of the image in the story sequence

        Returns: A pair of Image object and image file path
        """
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        filepath = os.path.join(workdir, f"image_{image_number}.png")
        img.save(filepath)
        return img, filepath
