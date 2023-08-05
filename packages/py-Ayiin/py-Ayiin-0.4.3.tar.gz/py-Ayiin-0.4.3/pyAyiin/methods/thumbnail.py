#
# Copyright (C) 2021-2022 by AyiinXd@Github, < https://github.com/AyiinXd >.
#
# This file is part of < https://github.com/AyiinXd/AyiinMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/AyiinXd/AyiinMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import os
import re
import textwrap

import aiofiles
import aiohttp
from PIL import (
    Image,
    ImageDraw,
    ImageEnhance,
    ImageFilter,
    ImageFont,
    ImageOps,
)

try:
    from youtubesearchpython.__future__ import VideosSearch
except ImportError:
    print("'youtubesearchpython' tidak terinstall\nMungkin beberapa modul tidak akan bisa digunakan.")
    pass


class Thumbnail(object):
    def changeImageSize(self, maxWidth, maxHeight, image):
        widthRatio = maxWidth / image.size[0]
        heightRatio = maxHeight / image.size[1]
        newWidth = int(widthRatio * image.size[0])
        newHeight = int(heightRatio * image.size[1])
        newImage = image.resize((newWidth, newHeight))
        return newImage


    async def gen_thumb(
        self, 
        client, 
        videoid,
    ):
        # cache = f"cache/{videoid}.png"
        # cache_thumb = f"cache/thumb{videoid}.png"
        # fonts = "assets/font.ttf"
        # fonts2 = "assets/font2.ttf"
        if not os.path.isdir('../cache/'):
            os.makedirs('../cache/')

        if os.path.isfile(f"cache/{videoid}.png"):
            return f"cache/{videoid}.png"

        url = f"https://www.youtube.com/watch?v={videoid}"
        try:
            results = VideosSearch(url, limit=1)
            for result in (await results.next())["result"]:
                try:
                    title = result["title"]
                    title = re.sub("\\W+", " ", title)
                    title = title.title()
                except BaseException:
                    title = "Unsupported Title"
                try:
                    duration = result["duration"]
                except BaseException:
                    duration = "Unknown Mins"
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                try:
                    views = result["viewCount"]["short"]
                except BaseException:
                    views = "Unknown Views"
                try:
                    channel = result["channel"]["name"]
                except BaseException:
                    channel = "Unknown Channel"

            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(
                            f"cache/thumb{videoid}.png", mode="wb"
                        )
                        await f.write(await resp.read())
                        await f.close()

            youtube = Image.open(f"cache/thumb{videoid}.png")
            image1 = self.changeImageSize(1280, 720, youtube)
            image2 = image1.convert("RGBA")
            background = image2.filter(filter=ImageFilter.BoxBlur(30))
            enhancer = ImageEnhance.Brightness(background)
            background = enhancer.enhance(0.6)
            Xcenter = youtube.width / 2
            Ycenter = youtube.height / 2
            x1 = Xcenter - 250
            y1 = Ycenter - 250
            x2 = Xcenter + 250
            y2 = Ycenter + 250
            logo = youtube.crop((x1, y1, x2, y2))
            logo.thumbnail((520, 520), Image.ANTIALIAS)
            logo = ImageOps.expand(logo, border=15, fill="white")
            background.paste(logo, (50, 100))
            draw = ImageDraw.Draw(background)
            font = ImageFont.truetype("./resources/font.ttf2", 40)
            font2 = ImageFont.truetype("./resources/font.ttf2", 70)
            arial = ImageFont.truetype("./resources/font.ttf2", 30)
            name_font = ImageFont.truetype("./resources/font.ttf", 35)
            para = textwrap.wrap(title, width=32)
            me = await client.get_me()
            uname = me.username
            music_name = f'{uname.upper()} UBOT' if uname else 'AYIIN UBOT'
            j = 0
            draw.text(
                (30, 5), f"{music_name}", fill="white", font=name_font
            )
            draw.text(
                (600, 150),
                "NOW PLAYING",
                fill="white",
                stroke_width=2,
                stroke_fill="white",
                font=font2,
            )
            for line in para:
                if j == 1:
                    j += 1
                    draw.text(
                        (600, 340),
                        f"{line}",
                        fill="white",
                        stroke_width=1,
                        stroke_fill="white",
                        font=font,
                    )
                if j == 0:
                    j += 1
                    draw.text(
                        (600, 280),
                        f"{line}",
                        fill="white",
                        stroke_width=1,
                        stroke_fill="white",
                        font=font,
                    )

            draw.text(
                (600, 450),
                f"Views : {views[:23]}",
                (255, 255, 255),
                font=arial,
            )
            draw.text(
                (600, 500),
                f"Duration : {duration[:23]} Mins",
                (255, 255, 255),
                font=arial,
            )
            draw.text(
                (600, 550),
                f"Channel : {channel}",
                (255, 255, 255),
                font=arial,
            )
            try:
                os.remove(f"cache/thumb{videoid}.png")
            except BaseException:
                pass
            background.save(f"cache/{videoid}.png")
            return f"cache/{videoid}.png"
        except Exception:
            results = VideosSearch(url, limit=1)
            for result in results.result()["result"]:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            return thumbnail
