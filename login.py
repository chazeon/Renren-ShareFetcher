import http.cookiejar, urllib.request, urllib.error, socket
from http.server import HTTPServer, BaseHTTPRequestHandler, CGIHTTPRequestHandler
import urllib.parse
import re, json, time, sys, os
import dirlib

class Login:
    _login_str = "email=&icode=&origURL=http%3A%2F%2Fwww.renren.com%2Fhome&domain=renren.com&key_id=1&captcha_type=web_login&password=&rkey=&f="
    _login_query = dict(urllib.parse.parse_qsl(_login_str))
    _login_query["email"] = ""
    _login_query["password"] = ""
    #print(_login_query)
    #_login_query.pop("rkey")   
    _login_str = urllib.parse.urlencode(_login_query)

    _cj = http.cookiejar.CookieJar()
    _opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cj))
    _incode_img = b""

    _mydirlib = dirlib.DirLib()

    def get_cookie(self):
        return self._cj

    def __init__(self):
        try:
            request_init = urllib.request.Request("http://www.renren.com/home")
            response_init = self._opener.open(request_init, timeout = 3)
        except urllib.error.URLError:
            print("You are currently offline!")
        except socket.gaierror:
            print("You are currently offline!")


    def do_login(self, email, password, icode = None):
        self._login_query["icode"] = icode
        if icode == None:
            self._login_query.pop("icode")
        else:
            self._login_query["icode"] = icode
        self._login_query["email"] = email
        self._login_query["password"] = password
        self._login_str = urllib.parse.urlencode(self._login_query)

        request_login = urllib.request.Request("http://www.renren.com/ajaxLogin/login?1=1", data = self._login_str.encode("utf-8"))
        response_login = self._opener.open(request_login)
        return_string = response_login.read()
        #print(return_string)
        return return_string

    def get_icode_image(self):
        request_icode = urllib.request.Request("http://icode.renren.com/getcode.do?t=web_login")
        response_icode = self._opener.open(request_icode)
        return_string = response_icode.read()
        return return_string

    def run_server(self):
        funcs = {"do_login_func": self.do_login, "get_incode_func": self.get_icode_image, "do_retrive_func": self.do_retrive_func}
        server = MyHTTPServer(funcs, ('', 8000), MyHandler)
        server.serve_forever()

    def do_retrive_func(self):
        pass


class MyHTTPServer(HTTPServer):
    def __init__(self, funcs, *args, **kw):
        HTTPServer.__init__(self, *args, **kw)
        self.get_incode_func = funcs["get_incode_func"]
        self.do_login_func = funcs["do_login_func"]
        self.do_retrive_func = funcs["do_retrive_func"]
        fsock = open("mime.json", "r")
        self.mimetype_library = json.load(fsock)
        fsock.close()

class MyHandler(CGIHTTPRequestHandler):
    _mydirlib = dirlib.DirLib()

    #print(cgi_directories)
    #print(CGIHTTPRequestHandler.cgi_directories)
    #cgi_directories = CGIHTTPRequestHandler.cgi_directories + ["/login"]
    def _set_headers_html(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()

    def _set_headers_text(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def _set_headers_jpeg(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()

    def _set_headers_json(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _set_headers_file(self, url):
        self.send_response(200)
        try:
            self.send_header('Content-type', self.server.mimetype_library[os.path.splitext(url.path[1:])[1]])
        except KeyError:
            self.send_header('Content-type', 'application/octet-stream')
        self.end_headers()

    def do_GET(self):
        #self.cgi_directories = CGIHTTPRequestHandler.cgi_directories + ["/verify", "/login"]
        url = urllib.parse.urlparse(self.path)
        if os.path.isfile(self._mydirlib.get_dir(os.path.join("www", url.path[1:]))) or url.path == "/":
            self._do_GET_file(url)
        else:
            if self._do_GET_CGI(url) != True:
                self._do_404()

    def _do_GET_file(self, url):
        if os.path.isfile(self._mydirlib.get_dir(os.path.join("www", url.path[1:]))):
            self._set_headers_file(url)
            fsock = open(self._mydirlib.get_dir(os.path.join("www", url.path[1:])), "rb")
            wfile_response = fsock.read()
            self.wfile.write(wfile_response)
            fsock.close()
            return True
        elif url.path == "/":
            self._set_headers_html()
            fsock = open(self._mydirlib.get_dir(os.path.join("www", "index.html")), "rb")
            wfile_response = fsock.read()
            self.wfile.write(wfile_response)
            fsock.close()
            return True
        else:
            return False

    def _do_GET_CGI(self, url):
        #print(self.cgi_directories)
        if url.path == "/verify":
            self._set_headers_jpeg()
            icode_image = self.server.get_incode_func()
            self.wfile.write(icode_image)
            return True
        if url.path == "/login":
            self._do_fake_POST()
        if url.path == "/retrive":
            self._do_retrive()
            self._set_headers_json()
            self.wfile.write(json.dumps("OK").encode())
        else:
            return False

    def _do_404(self):
        self.send_response(404)

    def _do_fake_POST(self):
        url = urllib.parse.urlparse(self.path)
        #if url.query == "":
            #print(self.rfile.readline())
        if url.path == "/login":
            query = dict(urllib.parse.parse_qsl(url.query))
            try:
                self._try_login(email = query["email"], password = query["password"], icode = query["icode"])
            except KeyError:
                self._try_login(email = query["email"], password = query["password"])
        else:
            self._do_404()

    def _do_retrive(self):
        self.server.do_retrive_func()

    def _try_login(self, email, password, icode = None):
        login_data = self.server.do_login_func(email, password, icode)
        self.wfile.write(login_data)


if __name__ == "__main__":
    mylogin = Login()
    mylogin.run_server()