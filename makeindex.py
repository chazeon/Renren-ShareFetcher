import json, os, dirlib

class MakeIndex:
	index = []
	_posts = []
	_mydirlib = dirlib.DirLib()
	#_dirs = {"share": "www/blog-json/share/", "collection": "www/blog-json/collection/"}
	def __init__(self, index_name, index_dir):
		self._posts = []
		self._dir = index_dir
		self._name = index_name
		self._filenames = os.listdir(self._dir)
		for i in self._filenames:
			self._posts.append(Post(self._mydirlib.get_dir(os.path.join(index_dir, i))))
		self.do_index()
		self.write_index()

	def do_index(self):
		self.index = []
		#print(len(self._posts))
		for i in self._posts:
			if i.get_check():
				self.index.append(i.get_index_item())

	def write_index(self):
		fsock = open(self._name + ".json", "w")
		json.dump(self.index, fsock)
		fsock.close()



class Post:
	def __init__(self, path):
		fsock = open(path, "rb")
		self._path = path
		self._post = json.loads(fsock.read().decode("utf-8"))
		
		if self.get_check():
			self._post_data = self._post["data"]

		fsock.close()

	def get_post(self):
		return self._post

	def get_post_data(self):
		return self._post_data

	def get_check(self):
		if self._post["code"] == 0:
			return True
		else:
			return False

	def get_title(self):
		return self._post_data["title"]

	def get_content(self):
		return self._post_data["content"]

	def get_date(self):
		return self._post_data["date"]

	def get_author_name(self):
		return self._post_data["authorName"]

	def get_post_id(self):
		return self._post_data["id"]

	def get_author_id(self):
		return self._post_data["authorId"]

	def get_raw_link(self):
		return "http://blog.renren.com/GetEntry.do?id=%s&owner=%s" % (str(self.get_post_id()), str(self.get_author_id()))

	def get_index_item(self):
		return {
			"title": self.get_title(),
			"author_name": self.get_author_name(),
			"author_id": self.get_author_id(),
			"post_id": self.get_post_id(),
			"date": self.get_date(),
			"url": os.path.split(self._path),
			"raw_link": self.get_raw_link(),
			"filename": os.path.split(self._path)[0].split("/")[-1] + "/" + os.path.split(self._path)[1]
		}

if __name__ == "__main__":
	_mydirlib = DirLib()
	dirs = {_mydirlib.get_dir("www/index/share"): _mydirlib.get_dir("www/blog-json/share"), _mydirlib.get_dir("www/index/collection"): _mydirlib.get_dir("www/blog-json/collection")}
	for (k, v) in dirs.items():
		MakeIndex(k, v)