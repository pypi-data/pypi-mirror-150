class BaseService:

    def __init__(self, path, base_url=None):
        self.__base_url = 'https://uploadio.basalam.com/api_v1.0/' if base_url is None else base_url
        self.__path = path

    def _set_base_file_url(self, url: str):
        self.__base_url = url

    def _get_url(self):
        return self.__base_url + self.__path
