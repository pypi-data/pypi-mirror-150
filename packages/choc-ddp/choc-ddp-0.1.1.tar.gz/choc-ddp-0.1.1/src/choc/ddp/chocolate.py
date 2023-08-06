import asyncio
from loguru import logger
from types import TracebackType
from typing import Optional,Type
from aiohttp import ClientSession

from choc.ddp.translate import Trans

def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

class Choco:
    
    trans : Optional[Trans] = None
    session: Optional[ClientSession] = None
    level_map: dict = {
        1: ["zh", "en", "de", "zh"],
        2: ["zh", "en", "de", "jp" ,"pt", "zh"],
        3: ["zh", "en", "de", "jp" ,"pt", "it", "pl", "bul", "est", "zh"]
    }
    
    def __init__(self,trans: Optional[Trans] = None) -> None:
        if trans is None:
            trans = Trans(session=self.session)
        self.trans = trans
    
    async def __aenter__(self) -> "Choco":
        self.session = ClientSession()
        await self.trans.initialization(session = self.session)
        return self

    async def __aexit__(
            self, 
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
        ) -> None:
        await self.session.close()
        
        
    async def transfer(self,content: str,level: int) -> str:
        target = self.level_map[level]
        for i in range(len(target)):
            if i == len(target)-1:
                break;
            content = await self.trans.dictionary(content,dst=target[i+1],src=target[i])
        return content
    
    async def deduplication(
            self,
            content: str = None,
            level: int = 1
        ) -> str:
        """_summary_

        Args:
            content (str, optional): _description_. Defaults to None.
            level (int, optional): _description_. Defaults to 1.
                1: zh -> en -> de -> zh
                2: zh -> en -> de -> jp -> pt -> zh
                3: zh -> en -> de -> jp -> pt -> it -> pl -> bul -> est -> zh
        """
        if content is None or not is_contains_chinese(content):
            logger.error(f"内容无效，仅支持中文")
        if level not in range(1,4):
            logger.error(f"level: {level}超出范围")
        return await self.transfer(content,level)
        
    
    
async def test():
    async with Choco() as c:
       await c.deduplication(input("待去重：\n"),3)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    