import os
import requests
import json
from typing import Any, Dict, List
from bs4 import BeautifulSoup
from neuralpit import Enviroment

class TikaConverterService():

    def __init__(self, tika_server_url) -> None:
        super().__init__()
        self.api_key = Enviroment.getApiKey()
        self.tika_server_url = tika_server_url

    def getFilePages(self, file_content) -> List[str]:
        headers = {'x-api-key':self.api_key, 'Accept': 'application/json'}
        resp = requests.put(self.tika_server_url+"/tika", headers = headers, data = file_content)
        resp_json = json.loads(resp.content)
        file_content = resp_json['X-TIKA:content']
        soup = BeautifulSoup(file_content, features="lxml")
        pages = soup.find_all("div", {"class": "page"})
        return [page.get_text() for page in pages] 


class LocalConverterService():

    def __init__(self) -> None:
        super().__init__()

    def getFilePages(self, file) -> List[str]:
        pass


