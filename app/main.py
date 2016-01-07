#!/usr/bin/env python


from GUI import *
from scanner_grc import *
from sniffer import *
from GSM_reciever import *

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
	    
class gui_thread(Qt.QThread):
	def __init__(self):
		
		Qt.QThread.__init__(self)
		parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
		(options, args) = parser.parse_args()
		if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
			Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
		self.qapp = Qt.QApplication(sys.argv)
		self.gui=GUI()
	def update1(self,L) :
		self.gui.draw1(L)
	def update2(self,L) :
		self.gui.draw2(L)
	def run(self):
		    self.gui.start()
		    self.gui.show()
		    def quitting():
			self.gui.stop()
			self.gui.wait()
		    self.qapp.connect(self.qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
		    
		    #self.gui = None #to clean up Qt widgets
		
class flow_thread(Qt.QThread):
	def __init__(self):
		Qt.QThread.__init__(self)
		self.tb=scanner_grc()
	def get_beacons(self) :
		return self.beacons 
	def get_progress(self) :

		return self.progress 		
	def run(self):
		airprobe=GSM_reciever(self.tb.get_fs())
		band=[[self.tb.get_f_900_b(),self.tb.get_f_900_e()],[self.tb.get_f_1800_b(),self.tb.get_f_1800_e()]]
		while (1) :
			self.progress=0 
			p=0
			i=0
			for b in band :
				self.beacons=[] 
				self.tb.set_fs(b[0])
				while (self.tb.get_fs()<=b[1]):
					print self.tb.get_fs(),
					p0=self.progress 
					self.progress=p/((band[0][1]-band[0][0]+band[1][1]-band[1][0])/200e3)*100
					if self.progress!=p0:
						self.emit(Qt.SIGNAL("p"))
					p=p+1
					self.tb.start()
					time.sleep(0.5)
					self.tb.stop()
					self.tb.wait()
					if(self.tb.threshold_result.last_state()==1) :
						self.beacons.append(self.tb.get_fs())
						airprobe.set_fc(self.tb.get_fs())
						airprobe.start()
						r=sniff()
						if r is not 0 :
							r['fc']=self.tb.get_fs()
						else :
							r=self.tb.get_fs()
						airprobe.stop()
						airprobe.wait()
						if i==0 :	
							self.emit(Qt.SIGNAL("list_updated1"))
							
							g.gui.update_text(r)
						else :
							self.emit(Qt.SIGNAL("list_updated2"))
													
							g.gui.update_text(r)
						print "found : ", self.beacons
					

						
					self.tb.set_fs(self.tb.get_fs()+200000)
					
					self.tb.threshold_result.set_last_state(0)
				i=1	    
	    
	    


if __name__ == '__main__':
    #~ sys.stdout = os.devnull
    #~ sys.stderr = os.devnull
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    sc = flow_thread()
    g=gui_thread()
    Qt.QObject.connect(sc, Qt.SIGNAL("list_updated1"),lambda : g.update1(sc.get_beacons()))
    Qt.QObject.connect(sc, Qt.SIGNAL("list_updated2"),lambda : g.update2(sc.get_beacons()))
    Qt.QObject.connect(sc, Qt.SIGNAL("p"),lambda : g.gui.progressBar.setValue(sc.get_progress()))

    g.start()
    sc.start()
    sys.exit(g.qapp.exec_())