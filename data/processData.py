import os

def readFile(filename): 
	with open(filename, 'r') as fp: 
		lines = fp.read()
		return lines

def getData(dir): 
	data = dict()
	for filename in os.listdir(dir):
		if (filename[0] != '.' and filename[0] != '_'): 
			data[filename] = readFile(dir + filename)

	return data


DATA_DIR = "results/"
data = getData(DATA_DIR)
print(data)