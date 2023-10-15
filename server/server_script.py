import socketserver
import http.server
import logging
import cgi
import os
import json
import shutil

PORT = 7800

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        response = {}

        try:
            mp4_file = form['mp4file']
            text_data = form.getvalue('textdata')

            print(mp4_file)

            #if mp4_file:
            mp4_file_path = os.path.join(os.getcwd(), "video.mp4")
            print("MP4 file path: %s", mp4_file_path)

            with open(mp4_file_path, 'wb') as f:
                shutil.copyfileobj(mp4_file.file, f)
            print("File MP4 saved successfully")

            # string
            print(text_data)

            text_file_path = os.path.join(os.getcwd(), "data.txt")

            # Salve os dados em um arquivo de texto
            with open(text_file_path, 'w') as text_file:
                text_file.write(text_data)
            print("File txt saved successfully")
            
            response['success'] = True
        except Exception as e:
            response['success'] = False
            response['error_message'] = str(e)

        # Retorne a resposta como JSON, independentemente do resultado
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving at port", PORT)
httpd.serve_forever()
