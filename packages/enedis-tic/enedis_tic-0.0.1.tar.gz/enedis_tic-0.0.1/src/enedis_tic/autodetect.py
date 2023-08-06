import asyncio

from src.enedis_tic import physical_layer
from serial.tools.list_ports import comports


async def autodetect():
    tasks = []
    for port in comports():
        tasks.append(asyncio.create_task(_detect(port.device)))
    await asyncio.gather(*tasks)
    return [t.result() for t in tasks if t.result()]


async def _detect(port):
    for mode in ('H', 'S'):
        try:
            res = await asyncio.wait_for(_detect_port(port, mode), 3)
        except Exception:
            continue
        else:
            return res
    return None


async def _detect_port(port, mode):
    reader = await physical_layer.serial_reader(port, mode)
    async for raw_frame in physical_layer.frame_iterator(reader):
        return {
            'port': port,
            'mode': mode,
            'sep': '\t' if '\t' in raw_frame else ' '
        }
