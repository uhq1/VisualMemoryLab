import os

class Trial: 
	def __init__(self, rawStimuli, rawResponses): 
		self.stimuli = []
		self.responses = []

		cnt = 0
		while '(' in rawStimuli: 
			idx1 = rawStimuli.index('(')
			idx2 = rawStimuli.index(')')
			instance = rawStimuli[idx1+1:idx2]
			spl = instance.split(',')
			word, typ, sec = spl[0], int(spl[1]), int(spl[2])
			self.stimuli.append((word, typ, sec))
			rawStimuli = rawStimuli[:idx1] + rawStimuli[idx2+2:]
			if cnt == 0: 
				self.numSec = sec
				self.image = (typ != 0)
			cnt += 1

		while '(' in rawResponses: 
			idx1 = rawResponses.index('(')
			idx2 = rawResponses.index(')')
			word = rawResponses[idx1+1:idx2]
			self.responses.append(word)
			rawResponses = rawResponses[:idx1] + rawResponses[idx2+2:]

	def getAccuraciesByImage(self): 
		accs = self.getAccuraciesByCategory()
		if len(accs) == 4: 
			return [sum(accs)/4.0]
		return accs

	def getAccuraciesByCategory(self): 
		if self.image: 
			numTotal = [0,0,0,0]
			numCorrect = [0,0,0,0]
			for (stimulus, typ, _) in self.stimuli: 
				if stimulus in self.responses: 
					numCorrect[typ-1] += 1
				numTotal[typ-1] += 1
			accuracies = []
			for i in range(4): 
				assert(numTotal[i] == 5)
				accuracies.append(numCorrect[i]*1.0/numTotal[i])
			return accuracies
		else: 
			numTotal = 0
			numCorrect = 0
			for (stimulus, typ, _) in self.stimuli: 
				if stimulus in self.responses: 
					numCorrect += 1
				numTotal += 1
			accuracies = []
			assert(numTotal == 20)
			return [numCorrect*1.0/numTotal]

class Subject: 
	def __init__(self, filename, rawData): 
		self.name = filename.replace(".txt", "")
		lines = rawData.split('\n')
		self.trials = [None, None, None, None]
		for idx in range(4): 
			trial = Trial(lines[idx], lines[idx+4])
			# sort back the random trial order
			if (not trial.image and trial.numSec == 1): 
				order = 0
			elif (trial.image and trial.numSec == 1): 
				order = 1
			elif (not trial.image and trial.numSec == 2): 
				order = 2
			else: 
				order = 3
			assert(self.trials[order] == None)
			self.trials[order] = trial
			
	def categoryRes2csv(self): 
		accs = []
		for t in self.trials: 
			for acc in t.getAccuraciesByCategory(): 
				accs.append(str(acc))

		csv = ",".join([self.name] + accs)
		return csv

	def imageRes2csv(self): 
		accs = []
		for t in self.trials: 
			for acc in t.getAccuraciesByImage(): 
				accs.append(str(acc))

		csv = ",".join([self.name] + accs)
		return csv

def readFile(filename): 
	with open(filename, 'r') as fp: 
		lines = fp.read()
		return lines

def getAllData(dir): 
	data = dict()
	for filename in os.listdir(dir):
		if (filename[0] != '.' and filename[0] != '_'): 
			data[filename] = readFile(dir + filename)
	return data

DATA_DIR = "results/"
allRawData = getAllData(DATA_DIR)
allData = dict()
csvsCat = []
csvsImg = []
hdrsCat = ['Subject', 'no image-short', 'context and color-short', 'no context and color-short', 'context and no color-short', 'no context and no color-short']
hdrsCat += ['no image-long', 'context and color-long', 'no context and color-long', 'context and no color-long', 'no context and no color-long']
hdrsImg = ['Subject', 'no image-short', 'image-short', 'no image-long', 'image-long']
for filename in allRawData: 
	rawData = allRawData[filename]
	subj = Subject(filename, rawData)
	csvsCat.append(subj.categoryRes2csv())
	csvsImg.append(subj.imageRes2csv())

csvCat = ",".join(hdrsCat) + "\n" + '\n'.join(csvsCat)
csvImg = ",".join(hdrsImg) + "\n" + '\n'.join(csvsImg)
print(csvImg)