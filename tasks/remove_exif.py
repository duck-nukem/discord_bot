import io
import logging
import os

from PIL import Image, UnidentifiedImageError
from discord import File


async def remove_processed_images(cleaned_images):
    cleaned_filenames = map(lambda f: f.filename, cleaned_images)

    for filename in cleaned_filenames:
        os.remove(filename)
        logging.info(f'{filename} cleansed & removed')


async def clean_attachment(attachment):
    image = await _open_image(attachment)

    if image is None:
        return None

    cleaned_image = await _remove_exif_data(image)
    cleaned_filename = f'clean_{attachment.filename}'
    cleaned_image.save(cleaned_filename)

    return File(cleaned_filename, spoiler=attachment.is_spoiler())


async def _remove_exif_data(image: Image):
    image_data = list(image.getdata())
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(image_data)

    return image_without_exif


async def _open_image(attachment):
    try:
        file_contents = await attachment.read()
        image = Image.open(io.BytesIO(file_contents))
    except UnidentifiedImageError as e:
        logging.info(f'{attachment.filename} is not an image, skipping exif removal')
        image = None

    return image
