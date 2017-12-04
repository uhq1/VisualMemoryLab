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
		(accs, numCorrect, imgCategCt, imgCategCtLong, imgCategCtShort, wrongAns) = self.getAccuraciesByCategory()
		if len(accs) == 4: 
			return ([sum(accs)/4.0],count)
		return (accs, numCorrect, imgCategCt, imgCategCtLong, imgCategCtShort, wrongAns)

	def promptCrResponseCategorization(self):
		cat = input("Categorize the response: PL (plurality) | TP (typo meaning preserved) | SYN (synonym less general)"+"\n")
		invalid = False
		if cat=="" or cat==" ":
			invalid = True
		else:
			if cat!= "PL" and cat!= "TP" and cat!= "SYN":
				invalid=True
		print(cat)
		print(invalid)		
		while invalid:
			cat = input("Categorize the response: PL (plurality) | TP (typo meaning preserved) | SYN (synonym less general)"+"\n")
			invalid = False
			if cat=="" or cat==" ":
				invalid = True
			else:
				if cat!= "PL" and cat!= "TP" and cat!= "SYN":
					invalid=True
		return cat

	def promptWrResponseCategorization(self):
		cat = input("Categorize the response: TP (typo meaning not preserved) | GEN (too general) | REL (DNE but related) | NR (DNE no relations)"+"\n")
		invalid = False
		if cat=="" or cat==" ":
			invalid = True
		else:
			if cat!= "TP" and cat!= "GEN" and cat!= "REL" and cat!= "NR":
				invalid=True	
		while invalid:
			cat = input("Categorize the response: TP (typo meaning not preserved) | GEN (too general) | REL (DNE but related) | NR (DNE no relations)"+"\n")
			invalid=False
			if cat=="" or cat==" ":
				invalid = True
			else:
				if cat!= "TP" and cat!= "GEN" and cat!= "REL" and cat!= "NR":
					invalid=True
		return cat 

	def initGradeCategories(self):
		gradeCrCateg=dict() #categorizing the non-exact answers that were graded as correct
		#legend: PL = plurality, TP = typo(meaning preserved), SYN = synonym(same or more precise)
		gradeCrCateg["PL"] = []
		gradeCrCateg["TP"] = []
		gradeCrCateg["SYN"] = []

		gradeWrCateg=dict() #categorizing the answers that were graded as incorrect
		#legend: TP = typo(meaning not preserved), GEN = too general, 
		#REL = DNE but related to something in list, NR = DNE and no relations to anything in list
		gradeWrCateg["TP"] = []
		gradeWrCateg["GEN"] = []
		gradeWrCateg["REL"] = []
		gradeWrCateg["NR"] = []
		return (gradeCrCateg, gradeWrCateg)

	def parseCategorization(self, gradeCateg, cat,response, typ, sec):
		catlist = cat.split(" ")
		for i in range(len(catlist)):
			if catlist[i] in gradeCateg:
				gradeCateg[catlist[i]] += [(response, typ, sec)]
			else:
				gradeCateg[catlist[i]] = [(response, typ, sec)]
		return gradeCateg

	def getAccuraciesByCategory(self): 
		getTypSec=True
		answerKey = dict()
		#numTotal=[0,0,0,0] if self.image else numTotal=0
		if self.image: 
			numTotal=[0,0,0,0] 
			imgCategCt = [0,0,0,0] #color-context, color-nocontext, nocolor-context, nocolor-nocontext
		else : 
			numTotal=0
		numCorrect=0
		#filling up the answer key
		for (stimulus, typ, sec) in self.stimuli:
			answerKey[stimulus] = (stimulus, typ, sec)
			if self.image: 
				numTotal[typ-1] += 1
			else: 
				numTotal += 1
			if getTypSec: #store type and duration of this answer key
				if typ==0: typp=0 
				else: typp=1
				if sec==1: secs=1
				else: secs=2
				getTypSec=False
		if self.image: 
			(gradeCrCateg, gradeWrCateg) = self.initGradeCategories()
			for response in self.responses:
				if response in answerKey:
					(stimulus, typ, sec) = answerKey[response]
					numCorrect += 1
					#store image category count total
					if typ != 0:
						imgCategCt[typ-1]+=1
				else:
					#prompt scoring of answer
					score = input(str(self.stimuli) +"\n"+response+"\n")
					while score!="yes" and score!="no":
						score = input(str(self.stimuli) +"\n"+response+"\n")				
					if score=="yes":
						ans = input("Which answer does it correspond to? \n")
						ansList = ans.split(" ")	
						ttyp = int(ansList[1])
						ssec = int(ansList[2])
						numCorrect += 1
						imgCategCt[ttyp-1]+=1
						gradeCrCateg = self.parseCategorization(gradeCrCateg,self.promptCrResponseCategorization(), response, typp, secs)
					else:
						gradeWrCateg = self.parseCategorization(gradeWrCateg,self.promptWrResponseCategorization(), response, typp, secs)
				print(imgCategCt)
			#accuracies = []
			#for i in range(4):
			#	assert(numTotal[i] == 5)
			#	accuracies.append(imgCategCt[i]*1.0/numTotal[i])
			return (numCorrect, imgCategCt, gradeCrCateg, gradeWrCateg)
		else: 
			(gradeCrCateg, gradeWrCateg) = self.initGradeCategories()
			for response in self.responses:
				if response in answerKey:
					(stimulus, typ, sec) = answerKey[response]
					numCorrect += 1
				else:
					score = input(str(self.stimuli) +"\n"+response+"\n")
					while score!="yes" and score!="no":
						score = input(str(self.stimuli) +"\n"+response+"\n")
					if score=="yes":
						ans = input("Which answer does it correspond to? \n")
						ansList = ans.split(" ")	
						ttyp = int(ansList[1])
						ssec = int(ansList[2])					
						numCorrect += 1
						gradeCrCateg = self.parseCategorization(gradeCrCateg,self.promptCrResponseCategorization(), response, typp, secs)
					else:
						gradeWrCateg = self.parseCategorization(gradeWrCateg,self.promptWrResponseCategorization(), response, typp, secs)
			#assert(numTotal == 20)
			return (numCorrect, None, gradeCrCateg, gradeWrCateg)

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
		print(self.trials[0].stimuli,"\nself.trials[0].stimuli\n",self.trials[1].stimuli,"\nself.trials[1].stimuli\n",self.trials[2].stimuli,"\nself.trials[2].stimuli\n",self.trials[3].stimuli,"\nself.trials[3].stimuli\n")

	def mergeDict(self, oldDict, newDict):
		for key in newDict:
			if key in oldDict:
				oldDict[key] += newDict[key]
			else:
				oldDict[key] = newDict[key]
		return oldDict	

	def categoryRes2csv(self): 
		#accs = [0.0,0.0,0.0,0.0] #noimageS, imageS, noimageL, imageL
		ct = [None,None,None,None] #noimageS, imageS, noimageL, imageL
		categSec = [None,None,None,None,None,None,None,None]
		crCatNoImg = dict()
		crCatImg = dict()
		wrCatNoImg = dict()
		wrCatImg = dict()
		tcount = 0
		for t in self.trials: 
			print(t, "self.trials[t]")
			print("\n")
			(numCorrect, numCImgCateg, CrCateg, WrCateg) = t.getAccuraciesByCategory();
			
			if tcount%2!=0:
				crCatImg = self.mergeDict(crCatImg,CrCateg)
				wrCatImg = self.mergeDict(wrCatImg,WrCateg)
			else:
				crCatNoImg = self.mergeDict(crCatNoImg,CrCateg)
				wrCatNoImg = self.mergeDict(wrCatNoImg,WrCateg)

			
			#tcount%2==0 no image
			if tcount//2==0: #short
				#accs[tcount%2]=accuracy
				ct[tcount%2]=str(numCorrect)
				if tcount%2!=0:
					print("SHORT IMAGE")
					for i in range(len(numCImgCateg)):
						categSec[i] = str(numCImgCateg[i])
			else:
				#accs[tcount%2+2]=accuracy
				ct[tcount%2+2]=str(numCorrect)
				if tcount%2!=0:
					for i in range(len(numCImgCateg)):
						categSec[i+4]=str(numCImgCateg[i])
			tcount+=1

		categ=[0,0,0,0]
		print(categSec, "categSec")
		for i in range(0, 4):
			categ[i]=str(int(categSec[i])+int(categSec[i+4]))

		sec=[0,0]
		sec[0]=str(int(ct[0])+int(ct[2]))
		sec[1]=str(int(ct[1])+int(ct[3]))

		img=[0,0]
		img[0]=str(int(ct[0])+int(ct[1]))
		img[1]=str(int(ct[2])+int(ct[3]))


		#print(accs)
		#acc2csv = ",".join([self.name] + accs)
		#accNoImg2csv = ",".join([self.name] + accsNoImg)
		imgSec2csv = ",".join([self.name] + ct)
		#ctNoImg2csv = ",".join([self.name] + ctNoImg)
		cat2csv = ",".join([self.name] + categ)
		sec2csv = ",".join([self.name]+sec)
		img2csv = ",".join([self.name]+img)
		catSec2csv = ",".join([self.name] + categSec)
		crCNI = (self.name,crCatNoImg)
		crCI = (self.name, crCatImg)
		wrCNI = (self.name, wrCatNoImg)
		wrCI = (self.name, wrCatImg)
			
		return (imgSec2csv, cat2csv, sec2csv, img2csv, catSec2csv, crCNI, crCI, wrCNI, wrCI)
	
def readFile(filename): 
	with open(filename, 'r') as fp: 
		lines = fp.read()
		return lines

def getAllData(dir): 
	data = dict()
	for filename in os.listdir(dir):
		if (filename[0] != '.' and filename[0] != '_'): 
			print(filename)
			print(readFile(dir+filename))
			data[filename] = readFile(dir + filename)
	return data

DATA_DIR = "results/"
allRawData = getAllData(DATA_DIR)
#print(allRawData)
#allData = dict()
#csvsAcc = []
csvsImgSec = []
csvsCat = []
csvsSec=[]
csvsImg=[]
csvsCatSec=[]
crCNIDict = dict()
crCIDict = dict()
wrCNIDict = dict()
wrCIDict = dict()
#hdrAcc = ['Subject','noimageS', 'imageS', 'noimageL', 'imageL']
hdrImgSec = ['Subject','noimageS', 'imageS', 'noimageL', 'imageL']
hdrSec = ['Subject','short','long']
hdrImg = ['Subject','no-image','image']
hdrCat=['Subject','color-context','color-nocontext','nocolor-context','nocolor-nocontext']
hdrCatSec = ['Subject', 'context and color-short', 'no context and color-short', 'context and no color-short', 'no context and no color-short']
hdrCatSec += ['context and color-long', 'no context and color-long', 'context and no color-long', 'no context and no color-long']

for filename in os.listdir(DATA_DIR): 
	rawData = allRawData[filename]
	print(rawData)
	subj = Subject(filename, rawData)
	(imgSec2csv, cat2csv, sec2csv, img2csv, catSec2csv, crCNI, crCI, wrCNI, wrCI) = subj.categoryRes2csv()
	#(acc2csv, count2csv, wrong2csv) = subj.imageRes2csv()
	#csvsAcc.append(acc2csv)
	csvsImgSec.append(imgSec2csv)
	csvsCat.append(cat2csv)
	csvsSec.append(sec2csv)
	csvsImg.append(img2csv)
	csvsCatSec.append(catSec2csv)
	crCNIDict[crCNI[0]] = crCNI[1]
	crCIDict[crCI[0]] = crCI[1]
	wrCNIDict[wrCNI[0]] = wrCNI[1]
	wrCIDict[wrCI[0]] = wrCI[1]
	print(filename,"DONE")
	print("Results:")
	#print("Accuracy noimageS imageS noimageL imageL : ",csvsAcc)
	print("Correct count noimageS imageS noimageL imageL : ",csvsImgSec)
	print("Correct count colorContext colorNocontext nocolorContext nocolorNocontext : ",csvsCat)
	print("Correct count short long: ",csvsSec)
	print("Correct count noimage image: ",csvsImg)
	print("Correct count category x duration",csvsCatSec)
	print("Correct categ no img: ", crCNI[0], crCNI[1])
	print("Correct categ img: ", crCI[0], crCI[1])
	print("Wrong categ no img: ", wrCNI[0], wrCNI[1])
	print("Wrong categ img: ", wrCI[0], wrCI[1])

#csvAcc = ",".join(hdrAcc) + "\n" + '\n'.join(csvsAcc)
csvImgSec = ",".join(hdrImgSec) + "\n" + '\n'.join(csvsImgSec)
csvCat = ",".join(hdrCat) + "\n" + '\n'.join(csvsCat)
csvSec = ",".join(hdrSec) + "\n" + '\n'.join(csvsSec)
csvImg = ",".join(hdrImg) + "\n" + '\n'.join(csvsImg)
csvCatSec = ",".join(hdrCatSec) + "\n" +'\n'.join(csvsCatSec)

#print(csvAcc)

print(csvImgSec)

print(csvCat)

print(csvSec)

print(csvImg)

print(csvCatSec)

print(crCNIDict)

print(crCIDict)

print(wrCNIDict)

print(wrCIDict)