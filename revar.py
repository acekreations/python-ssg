# Revar - Replace Variables
# Module for inserting variable in an html file using the '$VAR' syntax. Inspired by CodeKit's
# kit template system

def removeComm(i, source):
	source[i - 1] = source[i - 1].replace("<!--", "")
	source[i + 1] = source[i + 1].replace("-->", "")
	return source

def  revar(source, v):
	source = source.split()
	
	for i, word in enumerate(source):
		for key in v["fm"]:
			if("$" + key == word):
				source[i] = v["fm"][key]
				source = removeComm(i, source)
		if(word == "$url"):
			source[i] = v["url"]
			source = removeComm(i, source)
					
	return " ".join(source)
