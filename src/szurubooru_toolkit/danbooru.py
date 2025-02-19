from time import sleep

import requests
from loguru import logger
from pybooru import Danbooru as Danbooru_Module
from pybooru.exceptions import PybooruAPIError
from pybooru.exceptions import PybooruError
from pybooru.exceptions import PybooruHTTPError


class Danbooru:
    def __init__(self, danbooru_user, danbooru_api_key):
        if not danbooru_user == 'None' and not danbooru_api_key == 'None':
            self.client = Danbooru_Module('danbooru', username=danbooru_user, api_key=danbooru_api_key)
            logger.debug(f'Using Danbooru user {danbooru_user} with API key')
        else:
            self.client = Danbooru_Module('danbooru')
            logger.debug('Using Danbooru without user and API key')

    def get_by_md5(self, md5sum):
        for _ in range(1, 12):
            try:
                logger.debug(f'Trying to fetch result by md5sum {md5sum}')
                result = self.client.post_list(md5=md5sum)
                logger.debug(f'Returning result: {result}')

                break
            except (TimeoutError, PybooruError, PybooruHTTPError, PybooruAPIError):
                logger.debug('Got no result')
                sleep(5)
        else:
            logger.debug('Could not establish connection to Danbooru, returning None...')
            result = None

        return result

    def get_result(self, post_id):
        for _ in range(1, 12):
            try:
                result = self.client.post_show(post_id)
                logger.debug(f'Returning result: {result}')

                break
            except (TimeoutError, PybooruError, PybooruHTTPError, PybooruAPIError):
                logger.debug('Could not establish connection to Danbooru, trying again in 5s...')
                sleep(5)
        else:
            logger.debug('Could not establish connection to Danbooru. Skip tagging this post with Danbooru...')
            result = None

        return result

    def get_tags(self, result):
        result = result['tag_string'].split()
        logger.debug(f'Returning tags: {result}')

        return result

    def get_rating(self, result):
        result_rating = result['rating']
        logger.debug(f'Returning rating: {result_rating}')

        return result_rating

    @staticmethod
    def download_tags(query: str = '*', min_post_count: int = 10, limit: int = 100) -> list:
        """Download and return tags from Danbooru.

        Args:
            query (str, optional): Search for specific tag, accepts wildcard (*).
                If not specified, download all tags. Defaults to '*'.
            min_post_count (int, optional): The minimum amount of posts the tag should have been used in.
                Defaults to 10.
            limit (int, optional): The amount of tags that should be downloaded. Start from the most recent ones.
                Defaults to 100.

        Returns:
            list: A list with found tags.
        """

        tag_base_url = 'https://danbooru.donmai.us/tags.json'

        if limit > 1000:
            pages = limit // 1000
        else:
            pages = 1

        for page in range(1, pages + 1):
            tag_url = (
                tag_base_url
                + '?search[post_count]=>'
                + str(min_post_count)
                + '&search[name_matches]='
                + query
                + '&limit='
                + str(limit)
                + '&page='
                + str(page)
            )

            try:
                logger.info(f'Fetching tags from URL {tag_url}...')
                yield requests.get(tag_url, timeout=30).json()
            except requests.exceptions as e:
                logger.critical(f'Could not fetch tags: {e}')
