import logging
from tkinter import *
from tkinter import messagebox as mBox

logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
import math
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import time

import FileLoaderChooser

"""The PlotGui loads and flight locations across the US. """


class PlotGui(Frame):
    """init for PlotGui"""

    def __init__(self):
        super().__init__()
        self.data = []
        self.initUI()

    def initUI(self):
        """ build the GUI components via methods"""
        logging.debug('Launching UI')
        self.master.title("Data Plot Tool")
        self.master.iconbitmap(r'Cheezen-Web-2-Airplane.ico')
        self.pack(fill=BOTH, expand=True)
        # tkinter grid manager
        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        # methods that add and set the components to tk Frame
        self.createMenu()
        self.createListbox()
        self.addCheckBoxes()
        self.addPauseButton()
        self.createPlotCanvas()
        self.plotMap()
        self.plotData(0)

    def createMenu(self):

        """ Create the menu bar and all the menu items with commands and callbacks """
        menuBar = Menu()
        self.master.config(menu=menuBar)
        filemenu = Menu(menuBar, tearoff=0)
        fileFromMenu = Menu(menuBar, tearoff=0)
        filemenu.add_cascade(label="Load data from ", menu=fileFromMenu)
        fileFromMenu.add_command(label='Files...', command=lambda: self.dataTypeChooser('file'))
        fileFromMenu.add_command(label='API...', command=lambda: self.dataTypeChooser('api'))
        # fileFromMenu.add_command(label='Database...', command=lambda: self.dataTypeChooser('database'))
        fileFromMenu.add_command(label='Database...', command=lambda: self.popupmsg(msg="Not supported yet!"))
        filemenu.add_command(label="Save data set", command=lambda: self.popupmsg(msg="Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menuBar.add_cascade(label="File", menu=filemenu)

        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=lambda: self.popupmsg("About the Application",
                                                                          "Programmed by Jesse I. Follet\nFor Python 300 course"))
        menuBar.add_cascade(label="Help", menu=helpMenu)

    def dataTypeChooser(self, choice):
        """ called from the file load menu and launches the type of data to be loaded """
        self.data = []
        data = FileLoaderChooser.FileLoaderChooser(choice)
        logging.debug('Selected to load data by {}'.format(choice))
        if not data:
            mBox.showerror("Load Error", "Error loading data")
            return
        elif data == 'Cancel':
            return
        self.data = data
        self.setListbox(0)
        self.start_animation(choice)

    def start_animation(self, choice):
        """  Start the animations for live updating of the flight track points """
        logging.debug('Starting animations')
        if choice == 'file':
            self.ani = animation.FuncAnimation(self.f, self.animateFile, np.arange(0, 101), interval=5000)
        elif choice == 'api':
            self.ani = animation.FuncAnimation(self.f, self.animateApi, interval=1000)
        elif choice == 'database':
            pass
        self.c.draw()

    def createListbox(self):
        "Create a listbox that will list and allow multiple selection of data sets"
        frame = Frame(self, bd=2, relief=SUNKEN)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(frame, selectmode=SINGLE, bd=0, yscrollcommand=scrollbar.set)
        # listbox.bind('<ButtonRelease-1>', self.getListboxSelection)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)
        frame.grid(row=0, sticky="NSEW", padx=5, pady=5)
        self.listbox = listbox

    def setListbox(self, i):
        """ Set the listbox data based on the data object list index"""
        callsigns = self.data[i]['callsign']
        for item in callsigns:
            if item not in self.listbox.get(0, END):
                self.listbox.insert(END, item)

    def getListboxSelection(self):
        # returns the currently selected listbox item
        callsign = []
        idx = self.listbox.curselection()
        if idx:
            callsign = self.listbox.get(idx[0])
        return callsign

    def addCheckBoxes(self):
        """ Add checkbox(s)"""
        self.var = BooleanVar(value=False)
        checkbox = Checkbutton(self, text="Show Map", variable=self.var, command=self.showMap)
        checkbox.grid(row=1, sticky="NW", padx=5, pady=5)

    def addPauseButton(self):
        """Add pause button to gui"""
        hbtn = Button(self, text="Pause")
        hbtn.config(command=self.pause_callback)
        hbtn.grid(row=1, sticky="SEW", padx=5, pady=5)
        self.pause_button = hbtn

    def pause_callback(self):
        """Pauses the Callback"""
        logging.debug('Pausing data collection')
        hbtn = self.pause_button
        if hbtn['text'] == "Start":
            hbtn['text'] = "Pause"
        else:
            hbtn['text'] = "Start"

    def showMap(self):
        """Shows the US Map on the canvas axis"""
        if hasattr(self, 'anno'):
            self.anno.remove()
            del self.anno
        if self.var.get():
            self.plotMap(shader=True)
        else:
            self.plotMap()
        self.plotData(0)

    def createPlotCanvas(self):
        """Creates the plot canvas"""
        self.f = Figure()
        self.a = self.f.add_subplot(111)
        self.c = FigureCanvasTkAgg(self.f, self)
        self.c.get_tk_widget().grid(row=0, rowspan=2, column=1, sticky="NSEW", padx=5, pady=5)

    def plotMap(self, shader=False):
        """Plot the map on the map axis"""
        self.a.cla()
        m = Basemap(width=7500000, height=4000000, projection='lcc',
                    resolution='c', lat_1=25., lat_2=35, lat_0=40, lon_0=-100., ax=self.a)
        if shader:
            m.shadedrelief(scale=0.1)
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        parallels = np.arange(0., 81, 10.)
        m.drawparallels(parallels, labels=[False, True, True, False])
        meridians = np.arange(10., 351., 20.)
        m.drawmeridians(meridians, labels=[True, False, False, True])
        self.m = m

    def plotData(self, i):
        """Plot the flight data on to the map axis"""
        long_lat = self.querydata(i)
        if long_lat is not None and self.pause_button['text'] == "Pause":
            x = long_lat[:, 0]
            y = long_lat[:, 1]
            s = np.ones(len(long_lat)).tolist()
            rgb = plt.get_cmap('hsv')(np.linspace(0, 1, len(long_lat)))
            self.m.scatter(x, y, color=rgb, s=1.0)
            t = self.data[i]['time'].iloc[0]
            t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
            self.a.set_title(t)
            if hasattr(self, 'anno'):
                self.anno.remove()
                del self.anno
            callsign = self.getListboxSelection()
            if callsign:
                callsigns = self.data[i]['callsign']
                callsigns = callsigns.tolist()
                if callsign in callsigns:
                    ids = callsigns.index(callsign)
                    x_cs = x[ids]
                    y_cs = y[ids]
                    altitude = self.data[i]['altitude']
                    altitude = altitude.tolist()
                    self.anno = self.a.annotate(
                        ''.join([callsign.strip(), '\n', 'FL', str((int(math.floor(altitude[ids] * 3.28084) / 100)))]),
                        xy=(x_cs, y_cs), xycoords='data',
                        xytext=(x_cs + 100000, y_cs + 100000), textcoords='data',
                        arrowprops=dict(arrowstyle="->"),
                        bbox={'facecolor': 'yellow', 'alpha': 0.8, 'pad': 2},
                        fontsize=8
                    )

    def querydata(self, i):
        """grab the data from the Dataframe to send to plot"""
        logging.debug('Running Query')
        if self.data:
            longq = self.data[i]['longitude'].tolist()
            latq = self.data[i]['latitude'].tolist()
            longitude, latitude = self.m(longq, latq)
            # long, lat = self.m(latitude, longitude)
            long_lat = np.column_stack((longitude, latitude))
            self.setListbox(i)
        else:
            long_lat = None
        return long_lat

    def animateFile(self, i):
        """Animation callback for file load"""
        # self.querydata(i)
        self.plotData(i)

    def animateApi(self, i):
        """Animation callback for Opensky API load"""
        self.data = FileLoaderChooser.FileLoaderChooser('api')
        self.plotData(0)

    def popupmsg(self, title='OOPSY!', msg=''):
        "Generic popup message method for callback specifically"
        mBox.showinfo(title=title, message=msg)


def main():
    root = Tk()
    root.geometry("1280x720")
    app = PlotGui()
    app.mainloop()


if __name__ == '__main__':
    main()
