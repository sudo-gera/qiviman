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
from os.path import exists
from os.path import abspath
from os import chdir
import requests
from random import randint

def get_profile():
    s7 = requests.Session()
    s7.headers['Accept']= 'application/json'
    global qwtoken
    s7.headers['authorization'] = 'Bearer ' + qwtoken
    p = s7.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
    return p.json()

def balance(login):
    global qwtoken
    s = requests.Session()
    s.headers['Accept']= 'application/json'
    s.headers['authorization'] = 'Bearer ' + qwtoken
    b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + login + '/accounts')
    return b.json()

def fget(q,e):
 if type(e)==type(dict()):
  if q in e:
   return [e[q]]
  r=[]
  for w in e:
   r+=fget(q,e[w])
  return r
 elif type(e)==type(list()):
  r=[]
  for w in e:
   r+=fget(q,w)
  return r
 return []

def ls():
    q=get_profile()
    q=fget('personId',q)
    q=q[0]
    sleep(1/3)
    return balance(str(q))

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

pth=abspath(argv[0])
pth=pth[:-len(pth.split('/')[-1])]
chdir(pth)
os.system('git pull')
try:
 js=loads(open('../qiwiman.json').read())
except:
 open('../qiwiman.json','w').write(dumps({'qw':'','vk':''}))
 js=loads(open('../qiwiman.json').read())
try:
 qwtoken=js['qw']
except:
 qwtoken=''
 js['qw']=''
try:
 vktoken=js['vk']
except:
 vktoken=''
 js['vk']=''
open('../qiwiman.json','w').write(dumps(js))
#vktoken='10988f6b665ac9ee3134119bcf13904c479002e67798d70dbc8575a3359b3fb907cdf76f05df465d620b6'
hostName = 'localhost'
hostPort = randint(3000,9000)
minid=0
vkid=[367453637,225847803]

#url=input('server url:')
#api('groups.addCallbackServer?group_id=164701893&url={}&title=main'.format(url))


class MyServer(BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  path='.'+uqu(self.path)
  global qwtoken,vktoken
  if '?qw=' in path:
   qwtoken=path.split('?qw=')[1].strip()
  if '?vk=' in path:
   vktoken=path.split('?vk=')[1].strip()
  js['qw']=qwtoken
  js['vk']=vktoken
  open('../qiwiman.json','w').write(dumps(js))
  self.send_header("Content-type", "text/html; charset=utf-8")
  self.end_headers()
  self.wfile.write('''
  <form>
   <textarea name="qw">{}</textarea><br/>
   <input type="submit" value="save qiwi token">
  </form>
  <form>
   <textarea name="vk">{}</textarea><br/>
   <input type="submit" value="save vk token">
  </form>
  '''.format(qwtoken,vktoken).encode())

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
   if data['conversation_message_id']>minid and data['from_id'] in vkid:
    minid=data['conversation_message_id']
    m=data['text'].lower()
    id=data['peer_id']
    m=m.split()
    if m[0]=='ls':
     if qwtoken:
      bal=ls()
      try:
       bal=bal['accounts']
       bal=[[w['balance']['amount'],w['balance']['currency']] for w in bal if w['hasBalance']]
       d={643:'баланс в рублях: %s',0:'баланс в валюте номер %s по стандарту ISO-4217: %s'}
       bal=[d[w[1]]%w[0] if w[1] in d else d[0]%(w[1],w[0]) for w in bal]
       bal='\n'.join(bal)
      except:
       pass
      bal=str(bal)
      bal=bal.replace(qwtoken,'##token##')
      send(bal,id)
     else:
      send('qwtoken is not set',id)
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
       if qwtoken:
        mov=mv(m[1],m[2])
        try:
         if mov['transaction']['state']['code']=='Accepted':
          mov='transaction id: {}'.format(mov['transaction']['id'])
        except:
         pass
        mov=str(mov)
        mov=mov.replace(qwtoken,'##token##')
        send(mov,id)
       else:
        send('qwtoken is not set',id)
   self.wfile.write('ok'.encode())

st=1
while st:
 try:
  myServer = HTTPServer((hostName, hostPort), MyServer)
  st=0
 except:
  hostPort+=1
#print(asctime(), "Server Starts - %s:%s" % (hostName, hostPort))
print('port: {}'.format(hostPort))
try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print()
#print(asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
