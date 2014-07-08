import os, sys

class DirLib:
	def __init__(self, platform_string = None):
		if platform_string == None:
			self._platform = sys.platform
		else:
			self._platform = platform_string
		if self._platform == 'linux':
			self._linker = '/'
		elif self._platform == 'macosx':
			self._linker = '/'
		elif self._platform == 'windows':
			self._linker = '\\'
		else:
			self._linker = '/'

	def get_platform(self):
		return self._platform

	def get_dir_from_list(self, list_dir):
		return self._linker.join(list_dir)

	def get_list_from_dir(self, string_dir):
		list_split_bslash = []
		list_split_slash = string_dir.split("/")
		for i in list_split_slash:
			list_split_bslash.extend(i.split("\\"))
		return list_split_bslash

	def get_dir(self, string_dir):
		return self.get_dir_from_list(self.get_list_from_dir(string_dir))

if __name__ == "__main__":
	dirlib = DirLib()
	print(dirlib.get_dir("/"))
	print(dirlib.get_dir("\\Windows\\System32"))
	print(dirlib.get_dir("home/Project/renrenShare"))
	print(dirlib.get_dir("file.txt"))
	print(dirlib.get_dir("./a.exe"))

	dirlib_windows = DirLib("windows")
	print(dirlib_windows.get_dir("/"))
	print(dirlib_windows.get_dir("\\Windows\\System32"))
	print(dirlib_windows.get_dir("home/Project/renrenShare"))
	print(dirlib_windows.get_dir("file.txt"))
	print(dirlib_windows.get_dir("./a.exe"))