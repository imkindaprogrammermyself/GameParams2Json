import json,struct,codecs,zlib,pickle,sys

data = []
deflate = []
decom = []
pickle_data = []


def has_dict(o):
	try:
		o.__dict__
		return True
	except AttributeError:
		return False

class GPEncode(json.JSONEncoder):
	def default(self, o): # pylint: disable=E0202
		if has_dict(o):
			t = o.__dict__
			for key in t:
				if isinstance(t[key], str):
					try:
						t[key].decode('utf8')
					except:
						try:
							t[key] = t[key].decode('MacCyrillic')
						except:
							try:
								t[key] = t[key].encode('hex')
							except:
								pass
			return o.__dict__
print('Opening "GameParams.data".')
with open('./GameParams.data', 'rb') as f:
    byte = f.read(1)
    while byte:
        data.append(byte[0])
        byte = f.read(1)
    f.close()
print('Deflating data.')
deflate = struct.pack('B'*len(data), *data[::-1])
print('Decompressing data.')
decom = zlib.decompress(deflate)
pickle_data = pickle.loads(decom,encoding='MacCyrillic')
print('Writing data as "GameParams.json".')
json_data = json.dumps(pickle_data,cls=GPEncode,sort_keys=True,indent=4,separators=(',', ': '))
with open('./GameParams.json','w') as f:
    f.write(json_data)
    f.close()
print('Finished.')
