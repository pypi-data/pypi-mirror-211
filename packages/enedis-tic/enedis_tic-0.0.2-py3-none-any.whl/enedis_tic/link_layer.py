from datetime import datetime
from src.enedis_tic import physical_layer


async def frame_iterator(port, mode, sep='\t'):
    reader = await physical_layer.serial_reader(port, mode)
    async for raw_frame in physical_layer.frame_iterator(reader):
        try:
            yield frame(raw_frame[1:-1], sep)
        except RuntimeError:
            pass


def frame(raw, data_set_sep='\t'):
    if not raw:
        raise RuntimeError('Empty Frame')
    values = raw[1:-1].split('\r\n')
    return [{ds['label']: ds['data']} for ds in [data_set(v, data_set_sep) for v in values]]


def data_set(raw, sep='\t'):
    values = raw.split(sep)
    if not (3 <= len(values) <= 4):
        raise RuntimeError(f'Invalid DataSet: "{raw}"')
    SumChecker(raw).ensure_valid()
    res = {'label': values[0], 'data': values[-2]}
    if len(values) == 4:
        res['datetime'] = datetime.strptime(values[1][1:], '%y%m%d%H%M%S')
    return res


class SumChecker:
    def __init__(self, raw_data_set):
        self.raw_data_set = raw_data_set

    def verify(self):
        return (self.compute(self._payload) == self.given_checksum)\
               or (self.compute(self._older_payload) == self.given_checksum)

    def ensure_valid(self):
        if not self.verify():
            raise RuntimeError(f'Invalid checksum: "{self.raw_data_set}"')

    @staticmethod
    def compute(payload):
        s1 = sum([ord(c) for c in payload])
        return (s1 & 0x3F) + 0x20

    @property
    def _payload(self):
        return self.raw_data_set[:-1]

    @property
    def _older_payload(self):
        """For devices up to 2013"""
        return self.raw_data_set[:-2]

    @property
    def given_checksum(self):
        return ord(self.raw_data_set[-1])
