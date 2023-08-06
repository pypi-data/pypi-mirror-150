import json

import requests

from typing import Optional, List

from pydantic import BaseModel


class FileMinimal(BaseModel):
    id: int
    image_type: Optional[str]


class GetFileUrlsHandler:
    __base_file_url = 'https://uploadio.basalam.com/api_v1.0/'
    __path = 'files-urls'

    def __init__(self, files: List[FileMinimal], bucket: Optional[str] = None):
        self.bucket = bucket
        self.files = files

    def _set_base_file_url(self, url: str):
        self.__base_file_url = url

    def _get_url(self):
        return self.__base_file_url + self.__path

    def request_body(self):
        return {
            "bucket": self.bucket,
            "files": self.files
        }

    def get_links(self):
        return requests.get(self._get_url(), data=json.dumps(self.request_body()))
