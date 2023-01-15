from typing import Tuple, Optional

from PIL import Image, ImageDraw


class GradientImage:
    _DEFAULT_BACKGROUND_D_FACTOR: float = 0.5

    def __init__(
        self,
        color: Tuple[int, int, int],
        size: Tuple[int, int],
        factor: Optional[float] = None,
    ) -> None:
        self._main_color = color
        self._size = size
        self._factor = factor if factor else self._DEFAULT_BACKGROUND_D_FACTOR

    def get(self):
        return self._create()

    def _create(self) -> Image:
        gradient = Image.new("RGBA", self._size, color=0)
        draw = ImageDraw.Draw(gradient)
        for i, color in enumerate(
            self._interpolate(
                self._main_color,
                self._darken_color(self._main_color),
                self._size[0] + self._size[1],
            )
        ):
            draw.line([(i, 0), (0, i)], tuple(color), width=1)
        return gradient

    def _darken_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        return (
            int(color[0] - color[0] * self._factor),
            int(color[1] - color[1] * self._factor),
            int(color[2] - color[2] * self._factor),
        )

    @staticmethod
    def _interpolate(f_co, t_co, interval):
        det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
        for i in range(interval):
            yield [round(f + det * i) for f, det in zip(f_co, det_co)]


if __name__ == "__main__":
    gradient_image: Image = GradientImage(color=(240, 190, 90), size=(796, 1024)).get()
    gradient_image.show()
