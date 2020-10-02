import logging
import os

from discord import Message, Client, Status
from discord.ext.commands import Bot, Context, when_mentioned_or, MissingRequiredArgument

from banner import banner
from clients.discord import remove_exif_from_message_attachments
from tasks.youtube import find_first_youtube_match

client = Client()
bot = Bot(command_prefix=when_mentioned_or('!'), case_insensitive=True)


@bot.command(name='yt', help='Links a YouTube video by keyword, use like !yt r0bl0x gang')
async def link_video(ctx: Context, *, keyword):
    result = await find_first_youtube_match(keyword)

    await ctx.send(result)


@link_video.error
async def handle_link_video_errors(ctx, error):
    if isinstance(error, MissingRequiredArgument):
        await ctx.send('What should I search for? Try `!yt [keyword]`')


@bot.event
async def on_message(message: Message):
    # don't reply to self
    if message.author == bot.user:
        return

    await remove_exif_from_message_attachments(message)

    await bot.process_commands(message)


@bot.event
async def on_ready():
    logging.warning(banner)
    logging.info(f'Hello, I am {bot.user}')
    await bot.change_presence(status=Status.online)


if __name__ == '__main__':
    log_level = os.environ.get('LOG_LEVEL', logging.INFO)
    logging.basicConfig(
        format='[%(asctime)s - %(levelname)s]: %(message)s',
        level=log_level,
    )

    bot.run(os.environ['DISCORD_BOT_TOKEN'])
