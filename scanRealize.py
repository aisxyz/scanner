#coding:utf-8
import socket,threading,Queue,time
import wx

PortList=[21,22,23,25,80,135,137,139,445]
ThreadNum=30
TimeOut=3.0
PortNum=9
#OpenPort=[]
Lock=threading.Lock()
IsStop=False
IsFinish=False
ScanedPort=0
#TimeCount=0

def initGlobals():		#初始化必要的全局变量
	global IsStop,ScanedPort,IsFinish
	#OpenPort=[]
	IsStop=False
	IsFinish=False
	ScanedPort=0
	#TimeCount=0
	
class CountTime(threading.Thread):		#计时线程
	def __init__(self,showTime):
		threading.Thread.__init__(self)
		self.showTime=showTime
		self.timeStop=0
		self.timeStart=time.time()
	def run(self):
		while not IsFinish:
			while IsStop:
				time.sleep(1)
				self.timeStop+=1
			timeCount=0
			timeCount=int(time.time()-self.timeStart-self.timeStop)
			self.showTime.SetLabel(str(timeCount))
			
def queue(portList):
	portQueue=Queue.Queue(65535)
	for port in portList:
		portQueue.put(port)
	return portQueue
		
class ScanThread(threading.Thread):
	def __init__(self,scanIP,display):
		threading.Thread.__init__(self)
		self.scanIP=scanIP
		self.display=display
	def scanPort(self,port):
		global Lock,ScanedPort
		Lock.acquire()
		ScanedPort+=1
		#print 100*ScanedPort/PortNum,(ScanedPort,PortNum)
		Lock.release()
		address=(self.scanIP,port)
		sock=socket.socket()
		sock.settimeout(TimeOut)
		try:
			sock.connect(address)
			sock.close()
			#OpenPort.append(port)
		except:
			sock.close()
			return
		Lock.acquire()
		result="IP:%s\tOpen Port:%d\n" %(self.scanIP,port)
		#display.AppendText(result)
		result=self.display.GetValue()+result
		self.display.SetValue(result)
		self.display.SetStyle(0,len(result),wx.TextAttr('green'))
		Lock.release()
			
class ScanThreadSingle(ScanThread):
	def __init__(self,scanIP,display,portQueue):
		ScanThread.__init__(self,scanIP,display)
		self.portQueue=portQueue
	def run(self):
		#global ScanedPort,Lock
		while not self.portQueue.empty():
			#if IsFinish:
			#	return
			while IsStop:
				time.sleep(3)
			port=self.portQueue.get()
			#Lock.acquire()
			self.scanPort(port)
			#ScanedPort+=1
			#Lock.release()
			
class ScanThreadMul(ScanThread):
	def __init__(self,scanIP,display):
		ScanThread.__init__(self,scanIP,display)
	def run(self):
		#global ScanedPort,Lock
		for port in PortList:
			#if IsFinish:
			#	return
			while IsStop:
				time.sleep(3)
			#Lock.acquire()
			self.scanPort(port)
			#ScanedPort+=1
			#Lock.release()
			
def setPort(ports):
	global PortList
	PortList=[]
	portTemp=ports.split(',')
	for port in portTemp:
		if '-' not in port:
			if not port.isdigit():
				return False
			PortList.append(int(port))
		else:
			portRange=port.split('-')
			beginPort=portRange[0]
			endPort=portRange[1]
			if beginPort.isdigit() and endPort.isdigit():
				if int(endPort)>=65535:
					endPort=65535
				for p in range(int(beginPort),int(endPort)+1):
					PortList.append(p)
			else:
				return False
	return True
	
def singleIP(ip,display):
	global PortNum
	PortNum=len(PortList)
	threads=[]
	portQueue=queue(PortList)
	for i in range(ThreadNum):
		t=ScanThreadSingle(ip,display,portQueue)
		threads.append(t)
	for t in threads:
		t.start()
	#for t in threads:
	#	t.join(TimeOut)
		
def mulIP(ips,display):
	global PortNum
	threadList=[]
	(beginIP,endIP)=ips.split('-')
	try:
		socket.inet_aton(beginIP)
		socket.inet_aton(endIP)
	except:
		return
	ipRange=beginIP[0:beginIP.rfind('.')]
	begin=beginIP[beginIP.rfind('.')+1:]
	end=endIP[endIP.rfind('.')+1:]
	for tail in range(int(begin),int(end)+1):
		ip='%s.%d' %(ipRange,tail)
		t=ScanThreadMul(ip,display)
		threadList.append(t)
	PortNum=len(threadList)*len(PortList)
	for t in threadList:
		t.start()
	#for t in threadList:
	#	t.join(TimeOut)
	#test=0
	#while test<20:
	#	print PortNum