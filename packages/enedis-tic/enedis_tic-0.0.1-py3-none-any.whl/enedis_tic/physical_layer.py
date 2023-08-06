import serial_asyncio


HISTORIQUE = 'H'
STANDARD = 'S'
BAUDRATES = {
    HISTORIQUE: 1200,
    STANDARD: 9600
}
END_FRAME = b'\x03'


async def serial_reader(port, mode):
    reader, _ = await serial_asyncio.open_serial_connection(
        url=port,
        baudrate=BAUDRATES[mode],
        bytesize=serial_asyncio.serial.SEVENBITS,
        parity=serial_asyncio.serial.PARITY_EVEN,
        stopbits=serial_asyncio.serial.STOPBITS_ONE,
        rtscts=1
    )
    return reader


async def frame_iterator(reader):
    await reader.readuntil(END_FRAME)  # Skip truncated frame
    while True:
        frame = await reader.readuntil(END_FRAME)
        yield frame.decode('ascii')
