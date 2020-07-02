import os
import struct
import zlib
import pickle
import json
from concurrent.futures import ThreadPoolExecutor

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

entities_dir = os.path.join(__location__, "entities")


class GPEncode(json.JSONEncoder):
    def default(self, o):
        try:
            for e in ['Cameras', 'DockCamera', 'damageDistribution']:
                o.__dict__.pop(e, o.__dict__)
            return o.__dict__
        except AttributeError:
            return {}


def write_entities(data):
    _key, _value = data
    _ent_dir = os.path.join(entities_dir, _key)

    if not os.path.exists(_ent_dir):
        try:
            os.makedirs(_ent_dir)
        except OSError:
            pass
    for _d in _value:
        _d = dict(sorted(_d.items()))
        with open(os.path.join(_ent_dir, f"{_d['name']}.json"), "w") as ff:
            json.dump(_d, ff, indent=1)


if __name__ == '__main__':
    gp_file_path = os.path.join(__location__, 'GameParams.data')
    with open(gp_file_path, "rb") as f:
        gp_data: bytes = f.read()
    gp_data: bytes = struct.pack('B' * len(gp_data), *gp_data[::-1])
    gp_data: bytes = zlib.decompress(gp_data)
    gp_data: dict = pickle.loads(gp_data, encoding='windows-1251')
    gp_data: str = json.dumps(gp_data, cls=GPEncode, ensure_ascii=False)
    gp_data: dict = json.loads(gp_data)

    entity_types = {}

    for index, value in gp_data.items():
        data_type = value["typeinfo"]["type"]
        try:
            entity_types[data_type].append(value)
        except KeyError:
            entity_types[data_type] = [value]

    with ThreadPoolExecutor() as tpe:
        tpe.map(write_entities, [(k, v) for k, v in entity_types.items()])
