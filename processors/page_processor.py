import os
from typing import Tuple

import numpy
from fast_colorthief import get_dominant_color
from PIL import ImageFont, Image, ImageDraw
from data_models import StoryPageContent, StoryPage, AudioInfo, StorySize

from justifytext import justify

from util.gradient_image import GradientImage


class PageProcessor:
    _FONT: str = "fonts/Playfulist.ttf"
    _FONT_TITLES_SIZE: int = 18
    _WHITE_COLOR: Tuple[int, int, int] = (255, 255, 255)
    _BLACK_COLOR: Tuple[int, int, int] = (0, 0, 0)
    _BACKGROUND_TINT_FACTOR: float = 0.7
    _TEXT_JUSTIFICATION_WIDTH: int = 20
    _PAPER_BLEND_FACTOR: float = 0.1
    _PAPER_IMAGE_PATH: str = "./images/paper.jpeg"

    def create_page(
        self,
        workdir: str,
        story_page_content: StoryPageContent,
        audio: AudioInfo,
        story_size: StorySize,
    ) -> StoryPage:

        background_color = self._calculate_background_color(story_page_content)

        text_img: Image.Image = self._create_text_image(
            size=(story_size.text_part_width, story_size.text_part_height),
            bg_color=background_color,
            message=story_page_content.sentence,
            font=ImageFont.truetype(self._FONT, story_size.font_size),
            font_color=self._BLACK_COLOR,
        )

        if int(story_page_content.page_number) % 2 == 0:
            page_image: Image.Image = self._concat_horizontally(
                story_page_content.image, text_img
            )
        else:
            page_image = self._concat_horizontally(text_img, story_page_content.image)

        page_image = self._add_paper_effect(page_image)
        page_filepath = os.path.join(
            workdir, f"page_{story_page_content.page_number}.png"
        )
        page_image.save(page_filepath)
        return StoryPage(
            page_content=story_page_content,
            page_image=page_image,
            page_filepath=page_filepath,
            audio=audio,
        )

    def create_start_page(
        self, workdir: str, prompt: str, story_size: StorySize
    ) -> str:
        text_img = self._create_text_image(
            size=(story_size.page_width, story_size.page_height),
            bg_color=self._BLACK_COLOR,
            message=prompt,
            font=ImageFont.truetype(self._FONT, self._FONT_TITLES_SIZE),
            font_color=self._WHITE_COLOR,
            should_justify_text=False,
        )

        page_filepath = os.path.join(workdir, f"page_start.png")
        text_img.save(page_filepath)
        return page_filepath

    def create_end_page(self, workdir: str, story_size: StorySize) -> str:
        text_img = self._create_text_image(
            size=(story_size.page_width, story_size.page_height),
            bg_color=self._BLACK_COLOR,
            message="The End",
            font=ImageFont.truetype(self._FONT, self._FONT_TITLES_SIZE),
            font_color=self._WHITE_COLOR,
            should_justify_text=False,
        )

        page_filepath = os.path.join(workdir, f"page_end.png")
        text_img.save(page_filepath)
        return page_filepath

    def _add_paper_effect(self, page_image: Image) -> Image:
        paper: Image = Image.open(self._PAPER_IMAGE_PATH).convert(page_image.mode)
        paper = paper.resize(page_image.size)
        return Image.blend(page_image, paper, self._PAPER_BLEND_FACTOR)

    def _calculate_background_color(self, story_page_content: StoryPageContent):
        rgba_image = story_page_content.image.convert("RGBA")
        ndarray = numpy.array(rgba_image).astype(numpy.uint8)
        dominant_color = get_dominant_color(ndarray, quality=1)
        return self._lighten_color(dominant_color)

    def _lighten_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        return (
            int(color[0] + (255 - color[0]) * self._BACKGROUND_TINT_FACTOR),
            int(color[1] + (255 - color[1]) * self._BACKGROUND_TINT_FACTOR),
            int(color[2] + (255 - color[2]) * self._BACKGROUND_TINT_FACTOR),
        )

    @staticmethod
    def _concat_horizontally(
        image_left: Image.Image, image_right: Image.Image
    ) -> Image.Image:
        """Concatenate the given 2 images horizontally by putting them next to each other"""

        if image_left.height != image_right.height:
            raise RuntimeError(
                f"To concatenate 2 images horizontally,"
                f"the height of the 2 images must be the same: {image_left.height} != {image_right.height}"
            )
        dst = Image.new(
            "RGB", (image_left.width + image_right.width, image_left.height)
        )
        dst.paste(image_left, (0, 0))
        dst.paste(image_right, (image_left.width, 0))
        return dst

    def _create_text_image(
        self,
        size: Tuple[int, int],
        bg_color: Tuple[int, int, int],
        message: str,
        font: ImageFont.FreeTypeFont,
        font_color: Tuple[int, int, int],
        should_justify_text: bool = True,
    ) -> Image.Image:
        """Create an image with the give text on it

        Args:
            size: The size of the image to create (width, height)
            bg_color: Background color (r, g, b)
            message: The message/sentence to write on the image
            font: The font type to use for the text
            font_color: The text color (r, g, b)
            should_justify_text: A flag to break down the text into multiple lines

        Returns: A newly created image with the text on it
        """

        text_message = message

        if should_justify_text:
            text_message = "\n".join(justify(message, self._TEXT_JUSTIFICATION_WIDTH))

        width, height = size
        image = GradientImage(color=bg_color, size=size).get()
        draw = ImageDraw.Draw(image)
        x, y, w, h = draw.textbbox((0, 0), text_message, font=font)
        draw.text(
            ((width - w) / 2, (height - h) / 2),
            text_message,
            font=font,
            fill=font_color,
        )
        return image
