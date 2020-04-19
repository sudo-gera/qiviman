#!/data/data/com.termux/files/usr/bin/python
from http.server import BaseHTTPRequestHandler, HTTPServer
#import time
from urllib.request import urlopen as u
from urllib.parse import unquote as uqu
from json import loads as l
from sys import argv
import os
import random
from urllib.request import urlopen
from json import loads
from json import dumps
from urllib.parse import quote
from time import sleep
from time import time
from time import asctime
from traceback import format_exc as error
from os import popen
from random import shuffle
import requests

def ls(login):
    global qwtoken
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + qwtoken
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    return b.json()

def mv(sum_p2p, to_qw):
    global qwtoken
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + qwtoken
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"},"fields":{"account":""}}
    postjson['id'] = str(int(time() * 1000))
    postjson['sum']['amount'] = sum_p2p
    postjson['sum']['currency'] = '643'
    postjson['fields']['account'] = to_qw
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json = postjson)
    return res.json()

def api(path,data=''):
 sleep(1/3)
 if path and path[-1] not in '?&':
  if '?' in path:
   path+='&'
  else:
   path+='?'
 data=data.encode()
 global vktoken
 ret= loads(urlopen('https://api.vk.com/method/'+path+'v=5.101&access_token='+vktoken,data=data).read().decode())
 return ret
 print(asctime())

def send(text,id):
  text=str(text)
  while len(text)>4096:
   send(text[:4096],id)
   text=text[4096:]
  qq=api('messages.send?random_id='+str(time()).replace('.','')+'&peer_id='+str(id)+'&','message='+text)
  r=1
  if list(qq.keys())!=['response']:
   try:
    if qq['error']['error_code'] in [901,10,5]:
     r=0
   except:
    pass
   if r:
    print(qq)

vktoken='10988f6b665ac9ee3134119bcf13904c479002e67798d70dbc8575a3359b3fb907cdf76f05df465d620b6'
qwtoken='db5fa8f59f9669fec4756d29b96ae81b'

hostName = 'localhost'
hostPort = 3456

minid=0

class MyServer(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  path='.'+uqu(self.path)
  print(path)
  self.send_header("Content-type", "text/html; charset=utf-8")
  self.end_headers()
  self.wfile.write('ok'.encode())

 def do_POST(self):
  global admin
  lenn=int(self.headers['Content-Length'])
  path='.'+uqu(self.path)
  data=loads(self.rfile.read(lenn).decode())
  self.send_response(200)
  self.send_header("Content-type", "text/html; charset=utf-8")
  self.end_headers()
  if data['type']=='confirmation':
   self.wfile.write('2b1def61'.encode())
  elif data['type']=='message_new':
   data=data['object']['message']
   global minid
   if data['conversation_message_id']<=minid:
    return 0
   minid=data['conversation_message_id']
   m=data['text'].lower()
   id=data['peer_id']
   m=m.split()
   if m[0]=='ls':
    if len(m)<2:
     send('usage: ls <phone> \nexample: ls 79123456789',id)
    else:
     if m[1][0]=='+':
      m[1]=m[1][1:]
     send(ls(m[1]),id)
   if m[0]=='mv':
    if len(m)<3:
     send('usage: mv <sum> <phone> \nexample: mv 123.45 +79123456789',id)
    else:
     try:
      m[1]=float(m[1])
     except:
      send('usage: mv <sum> <phone> \nexample: mv 123.45 79123456789',id)
     else:
      if m[2][0]!='+':
       m[2]='+'+m[2]
      send(mv(m[1],m[2]),id)
  self.wfile.write('ok'.encode())

st=1
while st:
 try:
  myServer = HTTPServer((hostName, hostPort), MyServer)
  st=0
 except:
  hostPort+=1
print(asctime(), "Server Starts - http://%s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print()
print(asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
