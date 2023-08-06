from typing import Optional, Dict, List

from pydantic.main import BaseModel


class ArvanResponse(BaseModel):
    EXTRA_SMALL: Optional[str] = None
    EXTRA_LARGE: Optional[str] = None
    THUMBNAIL: Optional[str] = None
    ORIGINAL: Optional[str] = None
    MEDIUM: Optional[str] = None
    SMALL: Optional[str] = None
    LARGE: Optional[str] = None


class FilesUrlResponse(BaseModel):
    primary: Optional[str] = None
    extra_small: Optional[str] = None
    small_small: Optional[str] = None
    medium: Optional[str] = None
    large: Optional[str] = None
    arvan_urls: Optional[ArvanResponse] = None


class IndexFilesUrlResponse(BaseModel):
    __root__: Dict[str, FilesUrlResponse]


class FilesUrlsResponse(BaseModel):
    data: IndexFilesUrlResponse
