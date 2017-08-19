import tkinter as tk
from tkinter import *
from tkinter import messagebox as mBox
from tkinter import filedialog as fdlg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap
import FileLoaderChooser

class PlotGui:

    filelist = []

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Data Plot Tool")
        self.createMenu()
        self.createListbox()
        self.createPlotCanvas()
        # self.plotMap()
        self.plotData()




    def createMenu(self):
        menuBar = tk.Menu()
        self.win.config(menu=menuBar)

        filemenu = tk.Menu(menuBar, tearoff=0)
        # filemenu.add_command(label="Load data set", command=lambda: self.getFilename())
        fileFromMenu = tk.Menu(menuBar, tearoff=0)
        filemenu.add_cascade(label="Load data from ", menu=fileFromMenu)
        fileFromMenu.add_command(label='Files...', command=lambda: self.dataTypeChooser('file'))
        fileFromMenu.add_command(label='API...', command=lambda: self.dataTypeChooser('api'))
        fileFromMenu.add_command(label='Database...', command=lambda: self.dataTypeChooser('database'))
        filemenu.add_command(label="Save data set", command=lambda: self.popupmsg(msg="Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menuBar.add_cascade(label="File", menu=filemenu)


        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=lambda: self.popupmsg("About the Application", "Programmed by Jesse I. Follet\nFor Python 300 course"))
        menuBar.add_cascade(label="Help", menu=helpMenu)

    def dataTypeChooser(self, choice):
        self.data = FileLoaderChooser.FileLoaderChooser(choice)
        print(self.data)
        self.setListbox()


    def createListbox(self):
        "Create a listbox that will list and allow multiple selection of data sets"
        frame = Frame(self.win, bd=2, relief=SUNKEN)
        scrollbar = Scrollbar(frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(frame, selectmode=EXTENDED, bd=0, yscrollcommand=scrollbar.set)
        listbox.bind('<ButtonRelease-1>', self.getListboxSelection)
        scrollbar.config(command=listbox.yview)
        listbox.pack(side=LEFT, fill=BOTH, expand=1)
        frame.grid(row=0, sticky="NSEW", padx=5, pady=5)
        self.listbox = listbox

    def setListbox(self):
        print(self.data[0])
        callsigns = self.data[0]['callsign']
        print(callsigns)
        for item in callsigns:
            self.listbox.insert(tk.END, item)

    def createPlotCanvas(self):
        f = Figure()
        self.a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self.win)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=1, sticky="NSEW", padx=5, pady=5)
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def plotMap(self):
        m = Basemap(width=7500000,height=4000000,projection='lcc',
            resolution='c',lat_1=25.,lat_2=35,lat_0=40,lon_0=-100., ax=self.a)
        m.shadedrelief()
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()


    def plotData(self):
        pass

    def getListboxSelection(self, event):
        items = list(map(int, self.listbox.curselection()))
        print(items)

    def popupmsg(self, title='!', msg=''):
        "Generic popup message method for callback specifically"
        mBox.showinfo(title=title, message=msg)

    def querydata(self, i):
        self.data

    def animate(i):
        pass




if __name__ == '__main__':
    app = PlotGui()
    # app.win.geometry("1280x720")
    app.win.mainloop()

# TODO - 1.  animate with loop and read the dataframe load data classes.
# 2.  Fileloader will read database, write to file, animate will check file
# 3.  database loader will read a database from external connection - AWS?  Just localhost?
# 4.  Selector will show or unshow the callsign.
# 5.  put a callsign datalabel on latest data point
# 6.  Pretty up the axes
# 7.  Write some unit tests
# 8.  Make a map of the US
