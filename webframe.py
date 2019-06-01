from socket import *
import time
from websetting import *
from urls import *
from mao import *
class web(object):
	def __init__(self,addr):
		self.s = socket(AF_INET,SOCK_STREAM)
		self.s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
		self.s.bind(addr)
		
	def start(self):
		self.s.listen(5)
		while True:
			conn,Addr = self.s.accept()
			print("connect from ",Addr)
			please = conn.recv(1024).decode()
			import time
			time.sleep(0.1)
			position = conn.recv(1024).decode()
			print(please,position)
			if please == 'GET':
				if position[-5:] == ".html" or position =="/":
					statu,data = self.hand(position)
				else:
					statu,data = self.data(position)
			elif please == "PORT":
				pass
			conn.send(statu.encode())
			time.sleep(0.1)
			conn.send(data.encode())

	def data(self,position):
		for url,hand in urls:
			if position == url:
				return ('200',hand())
			else:
				return ('400','without me ,you could better')
	def hand(self,position):
		if position == '/':
			path = html_dir + '/index.html'
		else:
			path = html_dir + position
		try:
			f = open(path)
		except IOError:
			return ('400','we dont have this page')
		else:
			return ('200',f.read())
if __name__ == '__main__':
	w = web(addr)
	w.start() 