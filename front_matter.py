# Extracts 'front matter' from markdown files. Inspired by Jekylls use of YAML front matter
# For front matter to work markdown file should have an html comment tag to begin the file, 
# your data in the format of a key/value pair seperated by a line break not a comma, and a 
# html comment tag to end the front matter with two line breaks follow the comment tag.

def parse(content):
	fm = content.split("\n\n", 1)[0].split("\n")
	del fm[0], fm[-1]

	data = {}

	for f in fm:
		split = f.split(":")
		data[split[0]] = split[1]
	
	return data
