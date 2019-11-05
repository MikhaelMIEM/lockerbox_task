import sys, os
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from http.server import HTTPServer, BaseHTTPRequestHandler
from multiprocessing import Process

class PUTHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = self.rfile.read(length)
        filename, content = post_file_handler(body)
        with open(os.path.abspath("Saved_files/"+filename), 'wb') as output_file:
            output_file.write(content)
        self.send_response(200)


def post_file_handler(body):
    body = body.split(maxsplit=4)
    filename = body[4][0:body[4].find(b'\r\n')]
    filename = filename[filename.find(b'"')+1:filename.rfind(b'"')].decode()
    start_content_substr = b'\r\n\r\n'
    i = body[4].find(start_content_substr)
    content = body[4][i+len(start_content_substr):-46]
    return filename, content

def server():
    httpd = HTTPServer(('127.0.0.1', 9000), PUTHandler)
    try:
        httpd.serve_forever()
    except Exception:
        httpd.server_close()


if __name__ == '__main__':

    server_p = Process(target=server)
    server_p.start()

    app = QApplication(sys.argv)
    web = QWebEngineView()
    web.load(QUrl.fromLocalFile(os.path.abspath("index.html")))
    web.show()
    app.exec_()
    server_p.terminate()
