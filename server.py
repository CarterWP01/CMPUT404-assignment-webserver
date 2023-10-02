#  coding: utf-8 
import socketserver
import os


# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):

    def notFound(self, httpVersion):
        statusCode = "404 NOT FOUND"
        with open('www/error404.html') as myFile:
            return f"{httpVersion} {statusCode}\r\nContent-Type: {'text/html'}\n\n{myFile.read()}"

    def determineRequest(self, headers):
        request_lines = headers.split('\n')
        requestPath = request_lines[0].strip().split(' ')


        # statusCode = ""
        request = ''
        filePath = ''
        httpVersion = ''
        try:
            request = requestPath[0]
            filePath = requestPath[1]
            httpVersion = requestPath[2]
        except IndexError:
            filePath = '/'
        except Exception:
            pass

        if 'etc' in filePath or 'group' in filePath:
            return self.notFound(httpVersion)

        if request != 'GET':
            statusCode = '405 NoT FOUND'
            return f"{httpVersion} {statusCode}\r\n"

        if filePath[-1] == '/' or filePath == '/':
            filePath += 'index.html'

        #  base index

        try:
            with open(f"www{filePath}") as myFile:
                if '.' in filePath:
                    temp = filePath.split(".")
                    if temp[1] == 'css':
                        contentType = 'text/css'
                    elif temp[1] == 'html':
                        contentType = 'text/html'
                # if ending == 'index.html':
                #     contentType = 'text/html'
                fileInfo = myFile.read()
                statusCode = "200 OK"
                return f"{httpVersion} {statusCode}\r\nContent-Type: {contentType}\n\n{fileInfo}"

        except FileNotFoundError:
            return self.notFound(httpVersion)

        except Exception:
            pass

        try:
            with open(f"www{filePath}") as myFile1:
                myFile1.read()
        except OSError as e:
            if e.errno == 21:
                if filePath[-1] != '/':
                    statusCode = '301 Moved Permanently'
                    filePath += '/'
                    return f"{httpVersion} {statusCode}\r\nLocation: http://127.0.0.1:8080{filePath}"
            return self.notFound(httpVersion)
        except Exception as e:
            print(e)

    def handle(self):
        self.data = self.request.recv(1024).strip().decode()
        # print(f"Got a request of: {self.data}\n")
        response = self.determineRequest(self.data)

        self.request.sendall(bytearray(response, 'utf-8'))


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
