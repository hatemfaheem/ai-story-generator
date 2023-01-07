import os
from io import BytesIO

import openai
import requests
from PIL import Image


class ImageGenerator:
    @staticmethod
    def generate_image(prompt: str) -> str:
        """
        Generate a image for the given prompt/sentence.
        :param prompt: the text to generate an image for.
        :return: A url for the generated image.
        """
        response = openai.Image.create(prompt=prompt, n=1, size="256x256")
        print(f"Generated image for prompt '{prompt}': {response['data'][0]['url']}")
        return response['data'][0]['url']

    @staticmethod
    def download_image(workdir: str, url: str, prompt: str, image_number: str):
        """
        Download the image from the given url
        :param workdir: the workdir where to download the image
        :param url: The url of the image to download
        :param prompt: The prompt/sentence that used to generate the image. Will be added as a metadata in the image file
        :param image_number: the number of the image in the story sequence
        :return:
        """
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.prompt = prompt
        filename = os.path.join(workdir, f"image_{image_number}.png")
        img.save(filename)
        return img, filename
