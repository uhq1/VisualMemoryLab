import os

IMG_FOLDER = "images/"
objects = set()
for filename in os.listdir(IMG_FOLDER):
	if (filename[0] != '.' and filename[0] != '_'): 
		try: 
			s = filename[0:filename.index('-')]
			objects.add(s)
		except: 
			print("substring not found", filename)

objects = list(objects)
print(objects)


for word in objects: 
	for i in range(1,5): 
		filename = word + "-" + str(i) + ".png"
		if not os.path.exists(IMG_FOLDER + filename):
			print(filename)