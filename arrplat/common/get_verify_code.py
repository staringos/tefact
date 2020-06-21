import random
from io import BytesIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from arrplat.config import config

FONT_PATH = config.get("system", dict()).get("FONT_PATH")
if not FONT_PATH:
    raise Exception("Place config font path!")


class VerifyCodeImg:
    def __init__(self, width=150, height=30, code_count=4, font_size=35, point_count=0,
                 line_count=0, img_format='png', font_path=FONT_PATH):
        self.width = width
        self.height = height
        self.code_count = code_count
        self.font_size = font_size
        self.point_count = point_count
        self.line_count = line_count
        self.img_format = img_format
        self.font_path = font_path

    @staticmethod
    def get_random_color():
        c1 = random.randint(0, 255)
        c2 = random.randint(0, 255)
        c3 = random.randint(0, 255)
        return c1, c2, c3

    @staticmethod
    def get_random_str():
        random_num = str(random.randint(0, 9))
        random_char = random.choice([random_num, ])
        return random_char

    def get_verify_code_image(self):
        image = Image.new("RGB", (self.width, self.height), self.get_random_color())
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        font = ImageFont.truetype(FONT_PATH, size=self.font_size)

        temp = []
        for i in range(self.code_count):
            random_char = self.get_random_str()
            draw.text((10 + i * 30, -2), random_char, self.get_random_color(), font)
            temp.append(random_char)

        verify_str = "".join(temp)

        for i in range(self.line_count):
            x1 = random.randint(0, self.width)
            x2 = random.randint(0, self.width)
            y1 = random.randint(0, self.height)
            y2 = random.randint(0, self.height)
            draw.line((x1, y1, x2, y2), fill=self.get_random_color())

        for i in range(self.point_count):
            draw.point([random.randint(0, self.width), random.randint(0, self.height)], fill=self.get_random_color())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.get_random_color())

        bytes_io = BytesIO()
        image.save(bytes_io, self.img_format)
        byte_data = bytes_io.getvalue()
        bytes_io.close()

        return byte_data, verify_str
