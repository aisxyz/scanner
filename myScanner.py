#coding:utf-8
import wx
import scanRealize

explain=u'''Seeker 0.1说明：
	注:
	输入多个端口时以英文逗号相隔
	输入"-"表示连续范围
	
	默认扫描端口为:21,22,23,25,80,135,137,139,445
	单IP输入如:192.168.23.2或直接输入域名如：www.baidu.com
	IP范围输入如:192.168.23.1-192.168.23.100
	单端口输入如:80
	多端口输入如:23,80,135,200-500'''	
			
class MyScanner(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self,None,-1,'Seeker 0.1',
							size=(640,380),
							style=wx.DEFAULT_FRAME_STYLE^(wx.RESIZE_BORDER|wx.MAXIMIZE_BOX))
		panel=wx.Panel(self)
		
		#创建状态栏
		self.CreateStatusBar()
		self.SetStatusText(u'简易端口扫描器')
		
		#创建显示界面
		wx.StaticText(panel,-1,u'扫描结果:',(10,10))
		self.display=wx.TextCtrl(panel,-1,explain,(10,30),(320,260),
									wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH2)
		self.display.SetBackgroundColour('black')	#设置显示背景色为黑色
		self.display.SetStyle(0,len(explain),wx.TextAttr("green"))	#设置显示字体为绿色
		#self.display.SetDefaultStyle(wx.TextAttr('green'))
		
		#创建输入提示界面
		wx.StaticText(panel,-1,u'IP(或范围):',(345,10))
		self.ip=wx.TextCtrl(panel,-1,pos=(345,35),size=(240,20))
		wx.StaticText(panel,-1,u'Port(或范围):',(345,75))
		self.port=wx.TextCtrl(panel,-1,'21,22,23,25,80,135,137,139,445',pos=(345,100),size=(240,20))
		wx.StaticText(panel,-1,u'线程数:',(345,140))
		self.threadNum=wx.TextCtrl(panel,-1,'30',(385,140),(35,20))
		wx.StaticText(panel,-1,u'超时时间:',(450,140))
		self.timeout=wx.TextCtrl(panel,-1,'3000',(520,140),(40,20))
		wx.StaticText(panel,-1,'ms',(565,140))
		wx.StaticText(panel,-1,u'进度:',(345,180))
		self.gauge=wx.Gauge(panel,pos=(380,180),size=(190,10))
		self.startButton=wx.Button(panel,-1,u'开始扫描',(380,220))
		self.stopButton=wx.Button(panel,-1,u'暂停扫描',(480,220))
		wx.StaticText(panel,-1,u'用时:',(345,260),(35,-1))
		self.showTime=wx.StaticText(panel,-1,'0',(380,260),(15,-1))
		wx.StaticText(panel,-1,'s',(400,260))
		
		#绑定进度条事件和扫描事件
		#self.finish=False
		self.Bind(wx.EVT_IDLE, self.onIdle)
		self.Bind(wx.EVT_BUTTON,self.onStart,self.startButton)
		self.Bind(wx.EVT_BUTTON,self.onStop,self.stopButton)
		
	def onIdle(self,event):
		count=100*scanRealize.ScanedPort/scanRealize.PortNum
		self.gauge.SetValue(count)
		if count>=100:
			scanRealize.IsFinish=True
			#exit()
			
	def onStart(self,event):
		#if self.startButton.GetLabel()==u'开始扫描':
			#self.startButton.SetLabel(u'结束扫描')
		self.display.SetValue('')
		self.showTime.SetLabel('0')
		self.stopButton.SetLabel(u'暂停扫描')
		scanRealize.initGlobals()
		ips=self.ip.GetValue()
		ports=self.port.GetValue()
		if self.threadNum.GetValue().isdigit():
			scanRealize.ThreadNum=int(self.threadNum.GetValue())
			try:
				scanRealize.TimeOut=float(self.timeout.GetValue())
			except:
				wx.MessageBox(u'超时时间输入格式不正确，请检查！',u'温馨提示')
		else:
			wx.MessageBox(u'线程输入格式不正确，请检查！',u'温馨提示')
		if not scanRealize.setPort(ports):
			wx.MessageBox(u'端口输入格式不正确，请检查！',u'温馨提示')
			return
		scanRealize.CountTime(self.showTime).start()	#开始计时
		if '-' not in ips:
			scanRealize.singleIP(ips,self.display)
			#test.start(self.display)
		else:
			scanRealize.mulIP(ips,self.display)
		#while not self.finish:
		#	time.sleep(3)
		#wx.MessageBox(u'本次扫描结束',u'温馨提示')
		#else:
			#self.startButton.SetLabel(u'开始扫描')
			#scanRealize.IsFinish=True
			#self.finish=False
			
	def onStop(self,event):
		if self.stopButton.GetLabel()==u'暂停扫描':
			scanRealize.IsStop=True
			self.stopButton.SetLabel(u'继续扫描')
		else:
			scanRealize.IsStop=False
			self.stopButton.SetLabel(u'暂停扫描')
		
if __name__=='__main__':
	app=wx.PySimpleApp()
	frame=MyScanner()
	frame.Show()
	app.MainLoop()