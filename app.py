import os, shutil, front_matter, markdown, revar

build_path = "build/"

# check if build dir exists and remove it
if os.path.exists(build_path):
	shutil.rmtree(build_path)

# make build dir
os.mkdir(build_path)

posts_path = "src/posts/"
# list all posts
posts = os.listdir(posts_path)

post_data = []

# get content of each post file
for post in posts:
	f = open("src/posts/" + post, "r", encoding="utf-8")
	content = f.read()
	f.close()

	fm = front_matter.parse(content)
	path = post.split(".")[0]
	html = markdown.markdown(content)
	html = html.replace("\n", " ")
	slug = path.split("_")[1]
	date = path.split("_")[0]
	date = date[:4] + "-" + date[4:6] + "-" + date[6:]
	url = date + "/" + slug
	post_data.append({"path": path, "slug": slug, "url": url, "date": date, "fm": fm, "html": html})

# copy image folder and replace image urls
shutil.copytree("src/images", "build/images")
for post in post_data:
	post["html"] = post["html"].replace("/images/", "../../images/")

# get blog post template file and parse into before and after content segments
f = open("src/templates/post.html", "r", encoding="utf-8")
post_template = f.read()
f.close()
post_insert = post_template.split("<!-- content -->")

# build blog post pages and directories
for post in post_data:
	path = build_path + post['date'] + "/" + post['slug']
	os.makedirs(path)
	html = post_insert[0] + post["html"] + post_insert[1]
	f = open(path + "/index.html", "x")
	f.write(html)
	f.close()

# build home page
# get home page template
f = open("src/templates/home.html", "r", encoding="utf-8")
home_template = f.read()
f.close()
home_template = home_template.split("<!-- posts -->")

# get post summary template
f = open("src/templates/summary.html", "r", encoding="utf-8")
summary_template = f.read()
f.close()

# build summaries
summaries = []
for post in post_data:
	summary = revar.revar(summary_template, post)
	summary = summary.replace("/images/", "../../images/")
	summaries.append(summary)

# insert summaries into home template
home_template[1:1] = summaries
home = "".join(home_template)

# write index(home) file 
f = open(build_path + "index.html", "x")
f.write(home)
f.close()
