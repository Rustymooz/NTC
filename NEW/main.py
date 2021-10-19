from tkinter import *
import os

# To reload imports
import importlib
from tkinter import ttk

import GUI
import Classify

class Main:
    def __init__(self, frame):
        # Criar um style para modificar as cores da treeview
        s = ttk.Style(frame)
        s.theme_use("clam")


        # Create Project Frame
        frame_create = Frame(mainFrame)
        frame_create.grid(row=1, column=0)

        # Load Project Frame
        frame_load = Frame(mainFrame)
        frame_load.grid(row=1, column=1)

        # Label Project Frame
        frame_label = Frame(mainFrame, width=500, borderwidth=0)
        frame_label.grid(row=0, columnspan=2)

        # --------------------------------------------------------------------------------------------------------------------------------------------

        # Create Project Frame
        btn_start_project = Button(frame_create, text="Start New Project", height=5, width=20, command=self.createProject)
        btn_start_project.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky="nsew")

        # Load Project Button
        btn_load_project = Button(frame_load, text="Load Project", height=5, width=20, command=self.loadProject)
        btn_load_project.grid(row=1, column=2,  pady=10, padx=10, sticky="nsew")

        # Label
        label_welcome = Label(frame_label, text="      Net Traffic Classifier", font=("Arial", 20), height=3, width=20)
        label_welcome.grid(row=0, column=1, columnspan=1, pady=10, padx=10)

        # Configure columns and rows
        #Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 0, weight=1)

        #Grid.rowconfigure(frame, 1, weight=1)
        Grid.columnconfigure(frame, 2, weight=1)

    # --------------------------------------------------------------------------------------------------------------------------------------------
    def createProject(self):
        root = Toplevel()
        #root.config(background="gray69")

        # Creating tabs
        tabFrame = ttk.Notebook(root)

        # Creating Tab for Data Preparation
        tabDataPreparation = Frame(tabFrame, background="gray69")
        tabClassify = Frame(tabFrame, background="gray69")

        tabFrame.add(tabDataPreparation, text='Data Preparation')
        tabFrame.add(tabClassify, text='Classify')
        tabFrame.pack(expand=1, fill="both")

        classify = Classify.Classify(tabClassify)
        gui = GUI.GUI(tabDataPreparation, classify)

        # Start a new project
        GUI.GUI.chooseNameOfProject(gui)

        root.resizable(True, True)
        root.mainloop()

        gui.table.closeFiles()
        gui.projectDataLog.closeFile()

    def loadProject(self):
        root = Toplevel()
        # root.config(background="gray69")

        # Creating tabs
        tabFrame = ttk.Notebook(root)

        # Creating Tab for Data Preparation
        tabDataPreparation = Frame(tabFrame, background="gray69")
        tabClassify = Frame(tabFrame, background="gray69")

        tabFrame.add(tabDataPreparation, text='Data Preparation')
        tabFrame.add(tabClassify, text='Classify')
        tabFrame.pack(expand=1, fill="both")

        classify = Classify.Classify(tabClassify)
        gui = GUI.GUI(tabDataPreparation, classify)

        # Load Existing Project
        GUI.GUI.loadProject(gui)

        root.resizable(True, True)
        root.mainloop()

        gui.table.closeFiles()
        gui.projectDataLog.closeFile()

mainFrame = Tk()
mainFrame.title('NT Classifier')
#mainFrame.iconphoto('D:\\IPL\\3ºANO\\2_SEMESTRE\\PROJETO_INFORMATICO\\Projeto-Informatico\\FilesFiles\\icon.png')
mainFrame.geometry("400x260")
mainFrame.resizable(False, False)
mainWindow = Main(mainFrame)
mainFrame.mainloop()

