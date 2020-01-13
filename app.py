import os, shutil, front_matter, markdown, revar, json, time

start_time = time.time()

# get config options
with open("config.json") as json_file:
    config = json.load(json_file)

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
def get_home_template():
	f = open("src/templates/home.html", "r", encoding="utf-8")
	ht = f.read()
	f.close()
	ht = ht.split("<!-- posts -->")
	return ht

# get post summary template
f = open("src/templates/summary.html", "r", encoding="utf-8")
summary_template = f.read()
f.close()

# build summaries into dictionary where key represents pagination
summaries = {}
i = 1
page_num = 1
for post in post_data:
	summary = revar.revar(summary_template, post, page_num)
	summary = summary.replace("/images/", "../../images/")

	if page_num in summaries.keys():
		summaries[page_num].append(summary)
	else:
		summaries[page_num] = [summary]

	if i == config["posts_per_page"]:
		page_num += 1
		i = 1
	else:
		i += 1

def build_index(path, summaries, template):
	summaries = " ".join(summaries)
	template[1:1] = summaries
	home = "".join(template)
	f = open(path + "index.html", "x")
	f.write(home)
	f.close()

# create index.html files with pagination folders
for page in summaries:
	if page == 1:
		build_index(build_path, summaries[page], get_home_template())
	else:
		path = build_path + str(page) + "/"
		if not os.path.exists(path):
			os.makedirs(path)
		build_index(path, summaries[page], get_home_template())

print("Build time: %s seconds" % (time.time() - start_time))
