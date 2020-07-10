# apassist.py
#
# Peter Toth
# 6 May 2020

# !/usr/bin/env python

"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

"""

__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "viperx"

import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket

import base
import os, time
from output import *
from cgi import parse_header, parse_multipart
import imghdr
import shutil
import webbrowser

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    response = 200
    lastpost = 0

    def get_data(self):
        d = ""
        if not os.path.exists(base.PROGRAM_HOME_DIR + self.path):
            warning("404 '"+self.path+"' not found... serving /base/404.html")
            self.response = 404
            with open(base.PROGRAM_HOME_DIR + "404.html", 'r') as f:
                for line in f.readlines():
                    d += line
            return d.encode()
        with open(base.PROGRAM_HOME_DIR + self.path[1:].replace("/", "\\"), 'r') as f:
            info("serving '"+self.path+"'")
            self.response = 200
            for line in f.readlines():
                d += line
        return d.encode()

    def get_image_data(self):
        if not os.path.exists(base.PROGRAM_HOME_DIR + self.path):
            self.response = 404
            return b""
        with open(base.PROGRAM_HOME_DIR + self.path[1:].replace("/", "\\"), 'rb') as f:
            info("serving '" + self.path + "'")
            d = f.read()
        return d

    def encoded(self, string):
        return str(string).replace(" ","\\ ")


















    def do_GET(self):
        self.path = urllib.parse.unquote(self.path)
        data = ""

        if self.path == "/":
            info("redirecting '/' to '/base/index.html'")
            self.path = "/base/index.html"
        if self.path.endswith(".html"):
            content_type = "text/html"
            data = self.get_data()
        elif self.path.endswith(".css"):
            content_type = "text/css"
            data = self.get_data()
        elif self.path.endswith(".js"):
            content_type = "text/js"
            data = self.get_data()
        elif self.path.endswith(".png"):
            content_type = "image/png"
            data = self.get_image_data()
        elif self.path.endswith(".jpg") or self.path.endswith(".jpeg"):
            content_type = "image/jpeg"
            data = self.get_image_data()
        elif self.path.endswith(".ttf"):
            content_type = "font/ttf"
            data = self.get_image_data()


        elif self.path.startswith("/ajax*"):
            cmd = self.path.split("*")[1]
            if cmd == "getGallery":
                album_names = []
                albums = {}
                i = 0
                for album,dirs,files in os.walk(base.PROGRAM_HOME_DIR + "\\uploads\\"):
                    if dirs is not [] and len(album_names) < 1:
                        album_names = dirs
                    if len(files) > 0:
                        albums[album_names[i]] = [album, files]
                        i += 1
                print(str(albums))
                data += '<p>Click below to jump to each section!</p>'
                for key in albums:
                    data += '<a class="button" href="#album_'+key.replace(" ","-")+'">'+key+'</a><br><br>'
                for key in albums:
                    data += '<h3 id="album_'+key.replace(" ","-")+'">'+key+'</h3>'
                    for file in albums[key][1]:
                        data += '<div class="col-4-small col-6-small col-12-small"><img class="image fit" src="uploads/'+key+'/'+file+'" alt=""></div>'
                    data += "<br>"
            elif cmd == "clearGallery":
                shutil.rmtree(base.PROGRAM_HOME_DIR + "\\uploads\\")
                os.makedirs(base.PROGRAM_HOME_DIR + "uploads")
                data = "Successfully cleared the gallery!"
            elif cmd == "export":
                shutil.copytree(base.PROGRAM_HOME_DIR + "/uploads/", os.path.expanduser("~/Desktop") + "/APAssist", dirs_exist_ok=True)
                data = "Successfully exported your pictures to the desktop! You can now clear the gallery without losing data..."
            elif cmd == "getAddress":
                data = ':'.join([base.getIP(), "8000"])
            data = data.encode()
            content_type = "text/html"


        else:
            warning("couldn't identify request: "+self.path)
            self.path = "/base/404.html"
            content_type = "text/html"
            data = self.get_data()
        self.send_response(self.response)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(data)

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        pdict['CONTENT-LENGTH'] = int(self.headers['content-length'])
        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length),keep_blank_values=1)
        else:
            postvars = {}
        return postvars
















    def do_POST(self):
        info("received post data...")
        postvars = self.parse_POST()
        if not os.path.exists(base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0]):
            os.makedirs(base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0])
        for file in postvars['files']:
            fn = str(time.time()).replace(".","")
            with open(base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0] + "\\" + fn, 'wb+') as f:
                f.write(file)
                f.close()
            os.rename(base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0] + "\\" + fn,
                      base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0] + "\\" + fn + "."
                      + imghdr.what(base.PROGRAM_HOME_DIR + "uploads\\" + postvars['name'][0] + "\\" + fn))
        self.send_response(302)
        self.send_header("Location","/")
        self.end_headers()

















if __name__ == '__main__':
    base.setup_files()
    server_address = ('0.0.0.0',8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    webbrowser.open("http://localhost:8000/")
    print("listening on port 8000...")
    print("Open your web browser to http://localhost:8000/")
    print("You may minimize this window now!")
    httpd.serve_forever()