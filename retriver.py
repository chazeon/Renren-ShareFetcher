import re, json, os, sys, urllib.parse, urllib.request

import login, dirlib, makeindex

class LoginShare(login.Login):
    _mydirlib = dirlib.DirLib()

    _base_url_share = "http://share.renren.com/share/v7/"
    _share_link_pattern = "http://blog.renren.com/GetEntry.do\\?id=(\d+)&owner=(\d+)"
    _base_url_collection = "http://share.renren.com/share/collection/v7"
    _base_url_blog = "http://blog.renren.com/blog/"

    def do_retrive_func(self):
        request_home = urllib.request.Request("http://www.renren.com/")
        response_home = self._opener.open(request_home)
        response_home_content = response_home.read().decode("utf-8")
        self.set_uid(response_home_content)
        self.get_share()
        self.get_collection()
        _mydirlib = dirlib.DirLib()
        dirs = {_mydirlib.get_dir("www/index/share"): _mydirlib.get_dir("www/blog-json/share"), _mydirlib.get_dir("www/index/collection"): _mydirlib.get_dir("www/blog-json/collection")}
        try:
            for (k, v) in dirs.items():
                makeindex.MakeIndex(k, v)
        except FileNotFoundError:
            os.makedirs("www/index")
            for (k, v) in dirs.items():
                makeindex.MakeIndex(k, v)
        #print(dir(response_home))
        #print(response_home.getheaders())
        #print(response_home.getheader())

    def set_uid(self, string):
        #print(re.sub(",\s*\n\s*", "\n\"", re.sub("\s+:", "\":", re.findall("nx.user = {([^{}]+)}", string)[0] )))
        string_parsed = re.findall("nx.user = {([^{}]+)}", string)[0]
        #re.findall("nx.user = {([^{}]+)}", string)[0] )string_parsed = re.sub("[^(http)]\s*[^(http)]:", "\":", string_parsed)
        #string_parsed = re.sub(",\s*\n\s*", ",\"", string_parsed)
        #string_parsed = re.sub("\'", "\"", string_parsed)
        #string_parsed = re.sub("\n", "", string_parsed)
        #string_parsed = "\"" + string_parsed
        pattern = "(\S+)\s*:\s*[\"\'](\S+)[\"\']"
        string_parsed_dict = dict(re.findall(pattern, string_parsed))
        self._uid = string_parsed_dict["id"]

    def get_uid(self, string):
        self.set_uid()
        return self._uid

    def get_item_list(self, base_url, subdir):
        item_list = []
        i = 0
        while True:
            if subdir == "share":
                request_list = urllib.request.Request(base_url + self._uid + "?type=1&curpage=" + str(i))
            else:
                request_list = urllib.request.Request(base_url + "?type=1&curpage=" + str(i)) #TODO: need to be reconsidered
            print(base_url + self._uid + "?type=1&curpage=" + str(i))
            #print(i)
            response_list = self._opener.open(request_list, timeout = 3)
            response_list_content = response_list.read().decode("utf-8")
            item_list_page = re.findall(self._share_link_pattern, response_list_content)
            #print(item_list_page)
            if len(item_list_page) == 0:
                break
            item_list.extend(item_list_page)
            i += 1 
        return item_list

    def get_item(self, item_inf, subdir):
        """
        item_inf should be like (id, owner)
        """
        response_content_raw = b""
        while response_content_raw.decode("utf-8").startswith("{") == False:
            request_item = urllib.request.Request("%s%s/%s/a" % (self._base_url_blog, item_inf[1], item_inf[0]))
            response_item = self._opener.open(request_item)
            #print("%s%s/%s/a" % (self._base_url_blog, item_inf[1], item_inf[0]))
            #print("#1", item_inf)
            #response = json.load(response_item)
            response_content_raw = response_item.read()
            #print(response_content_raw.decode("utf-8")[:80])
            fsock = open(self._mydirlib.get_dir("www/blog-json/" + subdir + "/" + item_inf[0] + "-" + item_inf[1] + ".json"), "wb")
            fsock.write(response_content_raw)
            fsock.close()

    def get_items(self, base_url, subdir):
        item_list = self.get_item_list(base_url, subdir)
        #print(item_list)
        for item_inf in item_list:
            print(item_inf)
            self.get_item(item_inf = item_inf, subdir = subdir)

    def do_prepare_dir(self, subdir):
        try:
            for i in os.listdir(self._mydirlib.get_dir("www/blog-json/" + subdir)):
                os.remove(self._mydirlib.get_dir("www/blog-json/" + subdir + "/" + i))
        except FileNotFoundError:
            os.makedirs(self._mydirlib.get_dir("www/blog-json/" + subdir))

    def get_share(self):
        self.do_prepare_dir("share")
        self.get_items(self._base_url_share, subdir = "share")

    def get_collection(self):
        self.do_prepare_dir("collection")
        self.get_items(self._base_url_collection, subdir = "collection")



ls = LoginShare()
ls.run_server()
