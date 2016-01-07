
import PyQt4.Qwt5 as Qwt
from PyQt4 import Qt
from PyQt4 import QtCore,QtGui
from gnuradio import qtgui
from gnuradio import gr
from gnuradio import qtgui
class BarCurve(Qwt.QwtPlotCurve):

    def __init__(self, penColor=Qt.Qt.black, brushColor=Qt.Qt.white):
        Qwt.QwtPlotCurve.__init__(self)
        self.penColor = penColor
        self.brushColor = brushColor
        
    # __init__()
    
    def drawFromTo(self, painter, xMap, yMap, start, stop):
        """Draws rectangles with the corners taken from the x- and y-arrays.
        """

        painter.setPen(Qt.QPen(self.penColor, 2))
        painter.setBrush(self.brushColor)
        if stop == -1:
            stop = self.dataSize()
        # force 'start' and 'stop' to be even and positive
        if start & 1:
            start -= 1
        if stop & 1:
            stop -= 1
        start = max(start, 0)
        stop = max(stop, 0)
        for i in range(start, stop, 2):
            px1 = xMap.transform(self.x(i))
            py1 = yMap.transform(self.y(i))
            px2 = xMap.transform(self.x(i+1))
            py2 = yMap.transform(self.y(i+1))
            painter.drawRect(px1, py1, (px2 - px1), (py2 - py1))
	    #~ painter.drawText(Qt.QPoint(px2, 0.5),"test")  

    # drawFromTo()

# class BarCurve

class GUI(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Gui")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Gui")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "GUI")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
	self.beacons_900= beacons_900 = ''
	self.freq = freq = 50
	self.beacons_1800= beacons_1800 = ''
        ##################################################
        # Blocks
        ##################################################

        self.progressBar = Qt.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(70, 10, 531, 23))
        self.progressBar.setProperty("value", 0)

	self.top_layout.addWidget(self.progressBar)
        self._beacons_label_tool_bar = Qt.QToolBar(self)
        
      
	self.plot = Qwt.QwtPlot(self)
        self.plot.setTitle('900M')
	self.plot.plotLayout().setCanvasMargin(0)
	self.plot.setGeometry(QtCore.QRect(20, 20, 581, 141))
        self.plot.plotLayout().setAlignCanvasToScales(True)
	pen = Qt.QPen(Qt.Qt.DotLine)
        pen.setColor(Qt.Qt.black)
        pen.setWidth(0)
	#self.plot.setAxisAutoScale(Qwt.QwtPlot.xBottom,False)		
	self.plot.enableAxis(Qwt.QwtPlot.yLeft,False)
	self.plot.setAxisScale(Qwt.QwtPlot.xBottom,921.2e6,959.8e6,0)	
	#~ self.plot.setAxisAutoScale(Qwt.QwtPlot.yLeft)
	self.plot.setAutoReplot(True)
	self.top_layout.addWidget(self.plot)
	#~ plot de la bande 900
	#~ plot de la bande 1800M
	self.plot2 = Qwt.QwtPlot(self)
        self.plot2.setTitle('1800M')
	self.plot2.plotLayout().setCanvasMargin(0)
	self.plot2.setGeometry(QtCore.QRect(20, 300, 581, 400))
        self.plot2.plotLayout().setAlignCanvasToScales(True)
	pen = Qt.QPen(Qt.Qt.DotLine)
        pen.setColor(Qt.Qt.black)
        pen.setWidth(0)
	#self.plot.setAxisAutoScale(Qwt.QwtPlot.xBottom,False)		
	self.plot2.enableAxis(Qwt.QwtPlot.yLeft,False)
	self.plot2.setAxisScale(Qwt.QwtPlot.xBottom,1805.2e6,1879.8e6,0)	
	self.plot2.setAxisAutoScale(Qwt.QwtPlot.yLeft)
	self.plot2.setAutoReplot(True)
	self.top_layout.addWidget(self.plot2) 
	self.plainTextEdit = QtGui.QTextEdit(self)
        self.plainTextEdit.setReadOnly(True)
        self.top_layout.addWidget(self.plainTextEdit)
	self.plainTextEdit.append("scanning...")


        ##################################################
        # Connections
        ##################################################
        #self.__initZooming()
	#self.go(5)
    def __initZooming(self):
        """Initialize zooming
        """

        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOff,
                                        self.plot.canvas())
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.black))

    # __initZooming()
       
    def setZoomerMousePattern(self, index):
        """Set the mouse zoomer pattern.
        """

        if index == 0:
            pattern = [
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.LeftButton,
                                                 Qt.Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.MidButton,
                                                 Qt.Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.RightButton,
                                                 Qt.Qt.NoModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.LeftButton,
                                                 Qt.Qt.ShiftModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.MidButton,
                                                 Qt.Qt.ShiftModifier),
                Qwt.QwtEventPattern.MousePattern(Qt.Qt.RightButton,
                                                 Qt.Qt.ShiftModifier),
                ]
            self.zoomer.setMousePattern(pattern)
        elif index in (1, 2, 3):
            self.zoomer.initMousePattern(index)
        else:
            raise ValueError, 'index must be in (0, 1, 2, 3)'

    # setZoomerMousePattern()
    def clearZoomStack(self):
        """Auto scale and clear the zoom stack
        """

        self.plot.setAxisAutoScale(Qwt.QwtPlot.xBottom)
        self.plot.setAxisAutoScale(Qwt.QwtPlot.yLeft)
        self.plot.replot()
        self.zoomer.setZoomBase()

    # clearZoomStack()
 
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def update_text(self, output): 
	if type(output) is float :
		text="--------------------------------------------------------------- \n- frequency :"+str(output)
	else :
		if int(output['mnc'])==1 :
			operator =' (orange  TN) '
		elif int(output['mnc'])==2:
			operator =' (Tunisie Telecom) '
		elif int(output['mnc'])==3 :
			operator =' (Ooredoo TN) '
		text="--------------------------------------------------------------- \n- frequency : "+ str(output['fc']) + "\n- operator : "+ str(output['mcc']) + " "+str(output['mnc']) + operator +"\n- location (LAC/Cell ID) : " + str(output['lac'])+"/"+str(output['cid'])+ "\n - neighbor cells : " +str(output['larcfn'])
	self.plainTextEdit.append(text)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
	g.gui.set_beacons_label(freq)
	
    def draw1(self, L):
        """Create and plot a sequence of bars taking into account the controls
        """

        for bar in self.plot.itemList():
            if isinstance(bar, BarCurve):

                bar.detach()

        for f in L:

            bar = BarCurve(
                Qt.Qt.red,
                Qt.Qt.red,
                )
            bar.attach(self.plot)
	    bar.setData([f-100e3,f+100e3], [0, 1])
	
        #self.clearZoomStack()

    # go()
    def draw2(self, L):
        """Create and plot a sequence of bars taking into account the controls
        """
       

        for bar in self.plot2.itemList():
            if isinstance(bar, BarCurve):

                bar.detach()

        for f in L:

            bar = BarCurve(
                Qt.Qt.red,
                Qt.Qt.red,
                )
            bar.attach(self.plot2)
	    bar.setData([f-100e3,f+100e3], [0, 1])
	
        #self.clearZoomStack()

    # go()