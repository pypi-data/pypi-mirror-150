# -*- coding: utf-8 -*-
import re
import execjs
from loguru import logger
from aiohttp import ClientSession
from typing import Optional,NoReturn
from execjs._external_runtime import ExternalRuntime

from utils import JS_CODE

class Trans:
    
    __session: Optional[ClientSession] = None
    __headers: dict = None
    __token: Optional[str] = None
    __gtk: Optional[str] = None
    __javascript: ExternalRuntime.Context = execjs.compile(JS_CODE)
    
    def __init__(
            self,
            session: ClientSession = None,
            headers: dict = None,
        ):
        if headers is None:
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
        self.__session=session
        self.__headers=headers

    async def initialization(
            self,
            session: ClientSession = None,
        ) -> NoReturn:
        self.__session=session
        try:
            # 获得token和gtk
            # 必须要加载两次保证token是最新的，否则会出现998的错误
            await self.loadMainPage()
            await self.loadMainPage()
        except Exception as e:
            raise e
    

    async def loadMainPage(self) -> NoReturn:
        url = 'https://fanyi.baidu.com'
        async with self.__session.get(url, headers=self.__headers) as r:
            text = await r.text()
            self.__token = re.findall(r"token: '(.*?)',", text)[0]
            self.__gtk = re.findall(r"window.gtk = '(.*?)';", text)[0]


    async def langdetect(self, query):
        url = 'https://fanyi.baidu.com/langdetect'
        data = {'query': query}
        try:
            async with self.__session.post(url=url, data=data) as r:
                json = await r.json()
                if 'msg' in json and json['msg'] == 'success':
                    return json['lan']
                return None
        except Exception as e:
            raise e
        

    async def dictionary(self, query, dst='zh', src=None) -> Optional[str]:
        url = 'https://fanyi.baidu.com/v2transapi'
        sign = self.__javascript.call('token', query, self.__gtk)
        if not src:
            src = await self.langdetect(query)
        data = {
            'from': src,
            'to': dst,
            'query': query,
            'simple_means_flag': 3,
            'sign': sign,
            'token': self.__token,
        }
        try:
            async with self.__session.post(url=url, data=data) as r:
                if r.status == 200:
                    json = await r.json()
                    if 'error' in json:
                        raise Exception('baidu sdk error: {}'.format(json['error']))
                    return json['trans_result']['data'][0]['dst']
                return None
        except Exception as e:
            raise e
        