import os

from pyyoutube import Api


async def find_first_youtube_match(keyword: str):
    youtube = Api(api_key=os.environ['YOUTUBE_TOKEN'])
    results = youtube.search_by_keywords(
        q=keyword,
        search_type=('video',),
        count=1,
    ).items

    if len(results):
        msg = f'https://www.youtube.com/watch?v={results[0].id.videoId}'
    else:
        msg = 'I have found nothing'

    return msg
