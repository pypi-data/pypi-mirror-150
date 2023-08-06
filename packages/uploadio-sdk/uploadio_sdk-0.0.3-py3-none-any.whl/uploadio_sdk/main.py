from typing import List, Optional

from redis import Redis

from services.get_file_urls.get_file_urls_service import GetFileUrlsService


class UploadioConnection:
    def __init__(self,
                 base_url=None,
                 redis_connection: Redis = None,
                 redis_expire_time: int = None,
                 request_time_out: tuple = None
                 ):
        self.__base_url = base_url
        self.__redis_connection = redis_connection
        self.__redis_expire_time = redis_expire_time
        self.__request_time_out = request_time_out

    def get_files_urls(self, files: List[dict], bucket: Optional[str] = None,):
        GetFileUrlsService(
            files=files,
            bucket=bucket,
            redis_connection=self.__redis_connection,
            redis_expire_time=self.__redis_expire_time,
            base_url=self.__base_url,
            request_time_out=self.__request_time_out
        ).get_links()
