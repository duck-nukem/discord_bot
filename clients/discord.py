from tasks.remove_exif import clean_attachment, remove_processed_images


async def remove_exif_from_message_attachments(message):
    cleaned_files = [await clean_attachment(a) for a in message.attachments]
    cleaned_images = list(filter(None, cleaned_files))

    if not cleaned_images:
        return

    await message.add_reaction('⏳')
    msg = f'{message.author.mention} no more exif.'

    if message.content:
        msg += f'\n\n{message.author.mention} wrote "{message.content}"'

    await message.delete()
    await message.channel.send(msg, files=cleaned_images)
    await remove_processed_images(cleaned_images)
