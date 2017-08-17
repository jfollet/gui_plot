import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mBox
from tkinter import filedialog as fdlg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.basemap import Basemap

class PlotGui:

    filelist = []

    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Data Plot Tool")
        self.createMenu()
        self.createListbox()
        self.createPlotCanvas()

    def createMenu(self):
        menuBar = tk.Menu()
        filemenu = tk.Menu(menuBar, tearoff=0)
        filemenu.add_command(label="Load data set", command=lambda: self.getFilename())
        filemenu.add_command(label="Save data set", command=lambda: self.popupmsg(msg="Not supported yet!"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menuBar.add_cascade(label="File", menu=filemenu)
        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=lambda: self.popupmsg("About the Application", "Programmed by Jesse I. Follet\nFor Python 300 course"))
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.win.config(menu=menuBar)

    def createListbox(self):
        "Create a listbox that will list and allow multiple selection of data sets"
        listbox = tk.Listbox(self.win, selectmode=tk.EXTENDED)
        listbox.grid(row=0, sticky="NSEW", padx=5, pady=5)
        listbox.bind('<ButtonRelease-1>', self.getListboxSelection)
        self.listbox = listbox
        # for testing - remove when done
        for item in ["one", "two", "three", "four"]:
            listbox.insert(tk.END, item)

    def createPlotCanvas(self):
        f = Figure()
        self.a = f.add_subplot(111)
        canvas = FigureCanvasTkAgg(f, self.win)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=1, sticky="NSEW", padx=5, pady=5)
        # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        m = Basemap(width=7500000,height=4000000,projection='lcc',
            resolution='c',lat_1=25.,lat_2=35,lat_0=40,lon_0=-100., ax=self.a)
        m.shadedrelief()
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()

    def getListboxSelection(self, event):
        items = list(map(int, self.listbox.curselection()))
        print(items)

    def popupmsg(self, title='!', msg=''):
        "Generic popup message method for callback specifically"
        mBox.showinfo(title=title, message=msg)

    def getFilename(self):
        "Open dialog box, select and store filename into a global list"
        print(self.filelist)
        filename = fdlg.askopenfilename() # returns empty if canceled
        if filename:
            self.filelist.append(filename)


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