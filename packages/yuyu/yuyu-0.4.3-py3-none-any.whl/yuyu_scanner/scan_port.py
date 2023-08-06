import socket
import subprocess
import xml.etree.ElementTree as ET
import string
import random
import os
import socket

class check:
	def __init__(self, lists = []):
		self.result = []
		self.ip = []
		letters = string.ascii_lowercase
		rand =  ''.join(random.choice(letters) for i in range(10))
		self.name = "port_"+rand
		for data in lists:
			tmp_ip = socket.gethostbyname(data)
			if tmp_ip not in self.ip:
				open(self.name,"a").write(tmp_ip+"\n")
				self.ip.append(tmp_ip)
		self.scan()

	def scan(self):
		cmd = subprocess.getoutput("nmap -Pn -p 21,22,23,25,53,80,110,115,135,139,143,194,443,445,1433,3306,3389,5632,5900,25565 --open -oX - -iL "+self.name)
		tree = ET.fromstring(cmd)
		for i in tree.findall('host'):
			data = []
			ip = i.find("address").get("addr")
			for ii in i.findall("ports"):
				for iii in ii.findall('port'):
					port = iii.get("portid")
					service = iii.find("service").get("name")
					ps = port+"/"+service+"|"
					data.append([port, service, "open"])

			self.result.append([ip,data])
		os.remove(self.name)

