import json

import requests

from typing import Optional, List
from redis import Redis


from uploadio_sdk.schemas.get_file_urls_schema import FilesUrlsResponse, FilesUrlResponse
from uploadio_sdk.services.base_service import BaseService


class GetFileUrlsService(BaseService):
    def __init__(self,
                 files: List[dict],
                 bucket: Optional[str] = None,
                 redis_connection: Redis = None,
                 redis_expire_time: int = None,
                 base_url: str = None,
                 request_time_out: tuple = None
                 ):
        super().__init__(path='files-urls', base_url=base_url)
        self.__bucket = bucket
        self.__files = files
        self.__cached_files = []
        self.__redis_connection = redis_connection
        self.__redis_expire_time = redis_expire_time
        self.__request_time_out = request_time_out if request_time_out is not None else (2, 3)

    def request_body(self):
        return {
            "bucket": self.__bucket,
            "files": [file for file in self.__files if file['id'] not in self.__cached_files]
        }

    def get_links(self):
        cached_file_urls = {}
        requested_file_urls = {}
        cache_key = 'uploadio_sdk_get_file_urls_'
        if self.__redis_connection is not None:
            for file in self.__files:
                if self.__redis_connection.get(f'{cache_key}{file["id"]}') is not None:
                    cached_file_urls[file['id']] = FilesUrlResponse.parse_raw(
                        self.__redis_connection.get(f'{cache_key}{file["id"]}')
                    )
                    self.__cached_files.append(file['id'])
        if len(self.__files) != len(self.__cached_files):
            result = requests.get(self._get_url(), data=json.dumps(self.request_body()),
                                  timeout=self.__request_time_out)
            if result.status_code == 200:
                requested_file_urls = FilesUrlsResponse.parse_obj(result.json()).data.__root__
                for file_url in requested_file_urls:
                    if self.__redis_connection is not None:
                        self.__redis_connection.set(f'{cache_key}{file_url}',
                                                    value=requested_file_urls[file_url].json(),
                                                    ex=self.__redis_expire_time)
            else:
                raise Exception(f"{self._get_url()} not found")
        return {**requested_file_urls, **cached_file_urls}
