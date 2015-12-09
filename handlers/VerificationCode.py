import Image, ImageDraw, ImageFont, ImageFilter
import random
import StringIO


class VerificationCode():
    def rndChar(self):
        chrRange = range(65, 91) + range(97, 123) + range(48, 58)
        return chr(random.choice(chrRange))

    def rndColor(self):
        return (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255))

    def rndColor2(self):
        return (random.randint(32, 64), random.randint(32, 64), random.randint(32, 64))

    def createImg(self):
        width = 60 * 4
        height = 60
        code = ''
        image = Image.new('RGB', (width, height), (255, 255, 255))

        font = ImageFont.truetype('/usr/share/fonts/ARIAL.TTF', 36)

        draw = ImageDraw.Draw(image)

        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=self.rndColor())

        for t in range(4):
            c = self.rndChar()
            draw.text((60 * t + 10, 10), c, font=font, fill=self.rndColor2())
            code += c
        image = image.filter(ImageFilter.BLUR)

        return image, code
