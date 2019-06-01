import re
from socket import *
import time
from setting import *
import sys
from threading import Thread
import traceback
class http_server(object):
	def __init__(self,addr = ("0.0.0.0",80)):
		self.addr = addr
		self.s = socket(AF_INET,SOCK_STREAM)
		self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.s.bind(addr)
		self.s.listen(5)
	def hand(self):
		self.host = self.addr[0]
		self.port = self.addr[1]
		print("wait a minute")
		while True:
			try:
				conn,addr = self.s.accept()
				print("connect from ",conn.getpeername())
				t = Thread(target =self.server,args = (conn,))
				t.setDaemon(True)
				t.start()
			except KeyboardInterrupt:
				sys.exit("服务端退出")
			except:
				traceback.print_exc()
				continue
	def server(self,conn):
		data = conn.recv(4096)
		l = data.splitlines()
		pattern = r"(?P<please>[A-Z]+)\s+(?P<position>/\S*)"
		try:

			env = re.match(pattern,l[0].decode()).groupdict()
		except:
			requirements = "HTTP/1.1 500 server failed"
			requirements += '\r\n'
			require = "server error"
			message = require + requirements
			conn.send(message.encode())
			return
		statu,body = self.sendframe(env['please'],env['position'])
		head = self.head(statu)
		response = head + body
		print(response)
		conn.send(response.encode())
		conn.close()
	def sendframe(self,please,position):
		s=socket()
		s.connect(frameaddr)
		s.send(please.encode())
		time.sleep(0.1)
		s.send(position.encode())
		statu = s.recv(1024).decode()
		body = s.recv(4096).decode()

		return statu,body
	def head(self,statu):
		if statu == '200':
			head = 'HTTP/1.1 200 succeed\r\n'
			head +="\r\n"
		elif statu =='400':
			head = 'HTTP/1.1 400 failed\r\n'
			head +="\r\n"
		return head
if __name__ == "__main__":
	k = http_server(addr)
	k.hand()
