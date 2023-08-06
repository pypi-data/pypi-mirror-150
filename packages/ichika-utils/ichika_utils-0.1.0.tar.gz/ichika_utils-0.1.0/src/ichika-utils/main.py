import asyncio

class IchikaUtils:
    def __init__(self):
        self.self = self
        
    async def init(self):
        for _ in range(10):
            await asyncio.sleep(3)
            print("hello world")