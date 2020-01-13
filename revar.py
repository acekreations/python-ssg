# Revar - Replace Variables
# Module for inserting variable in an html file using the '$VAR' syntax. Inspired by CodeKit's
# kit template system

def remove_comment(i, source):
	source[i - 1] = source[i - 1].replace("<!--", "")
	source[i + 1] = source[i + 1].replace("-->", "")
	return source

def  revar(source, v, page_num):
	source = source.split()

	for i, word in enumerate(source):
		for key in v["fm"]:
			if "$" + key == word:
				source[i] = v["fm"][key]
				source = remove_comment(i, source)
		if word == "$url":
			if page_num == 1:
				source[i] = v["url"]
				source = remove_comment(i, source)
			else:
				source[i] = "../" + v["url"]
				source =  remove_comment(i, source)

	return " ".join(source)
