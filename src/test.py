import asyncio
import time

def hola():
    print("hola")
    time.sleep(1)

loop = asyncio.get_event_loop()
loop.run_in_executor(hola())