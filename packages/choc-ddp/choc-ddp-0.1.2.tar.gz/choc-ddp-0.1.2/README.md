# choc_ddp

```python
pip install choc-ddp

#推荐
poetry add choc-ddp
```

示例
```python
import asyncio 
from loguru import logger
from choc.ddp.chocolate import Choco

async def test():
    async with Choco() as c:
       resp = await c.deduplication(input("待去重：\n"),3)
       logger.info(resp)
       
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
```