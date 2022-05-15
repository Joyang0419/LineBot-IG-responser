import os
import pathlib
import urllib.request
import json
from typing import List, Literal, Union

from instagram_scraper.app import InstagramScraper

from src.configs.config import Settings

IG_ACCOUNT_CONFIG = Settings().ig_account_config
PHOTOS_PATH = \
    pathlib.Path(__file__).parent.parent.parent.resolve().joinpath('photos')


class ServiceInstagramScraper(InstagramScraper):
    MEDIA_TYPES = Literal['image', 'video', 'story-image', 'story-video']

    def __init__(
            self,
            username: str,
            password: str,
            get_media_types: List[Union[MEDIA_TYPES]]
            ,
            get_chunk_size: int = 0,
            latest: bool = True
    ):
        InstagramScraper.__init__(
            self,
            login_user=username,
            login_pass=password,
            get_media_types=get_media_types,
            max=get_chunk_size,
            latest=latest
        )

    def start_crawl(self, account: str):
        self.authenticate_with_login()
        shared_data = self.get_shared_data_userinfo(username=account)

        if not shared_data:
            return

        media_files = self.query_media_gen(shared_data)

        data: dict = dict(
            (item['shortcode'], item['display_url'])
            for item in media_files
        )

        with open(
            file=f'{PHOTOS_PATH}/{account}.txt',
            mode='w'
        ) as f:
            f.write(json.dumps(data))

    @staticmethod
    def _save_image(url: str, filename: str):
        urllib.request.urlretrieve(
            url=url,
            filename=filename
        )
