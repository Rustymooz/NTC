import csv
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox, ttk

import pandas
import pandas as pd
from shutil import copyfile
import datetime
from tkinter.ttk import Notebook
import numpy
from sklearn import preprocessing as pp
from sklearn import model_selection as ms
# import keras_preprocessing
# import category_encoders as ce
from pathlib import Path
import File
import Table
import LogFile
import ProjectLogFile
import Classify as cl


class GUI:

    def __init__(self, master, classifySide):
        self.classifySide = classifySide
        self.filePath = None
        self.copiedFilePath = None
        self.table = None
        self.targetColumm = None
        self.target_column_index = None
        self.sysLogFile = None
        self.projectSteps = []
        self.log = None
        self.projectDataLog = None
        self.projectName = None
        self.projectPath = None

        '''
        # Create Menu Bar (Menu suspenso no topo da aplicação)
        menuBar = Menu(master)
        master.config(menu=menuBar)

        # Create item in Menu Bar
        file_menu = Menu(menuBar, tearoff=0)
        # Add item to the Menu Bar
        menuBar.add_cascade(label='File', menu=file_menu)

        # Add sub-items to the first menu item
        file_menu.add_command(label="Open File", command=self.chooseNameOfProject)
        file_menu.add_command(label="Create New Project", command=self.showDataInTable)
        file_menu.add_command(label="Load Project", command=self.loadProject)
        file_menu.add_separator()
        # Alteracao
        file_menu.add_command(label="Exit", command=master.quit)
        '''

        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        # ---------------------------------------------------- FRAMES -------------------------------------------------------------------------
        # FRAMES
        fileFrame = Frame(master, background="gray69")
        fileFrame.grid(row=0, column=0, sticky=E + W + N + S)
        fileFrame.grid_rowconfigure(0, weight=1)
        fileFrame.grid_columnconfigure(0, weight=3)
        fileFrame.grid_columnconfigure(1, weight=1)

        fileNameFrame = LabelFrame(fileFrame, text="File", background="gray69")
        fileNameFrame.grid(row=0, column=0, padx=3, pady=3, sticky=E + W + N + S)
        fileNameFrame.grid_rowconfigure(0, weight=1)
        fileNameFrame.grid_columnconfigure(0, weight=3)

        # Frame For Data Table
        dataTableFrame = LabelFrame(fileFrame, text="Data Table", background="gray69")
        dataTableFrame.grid(row=0, column=1, padx=3, pady=3, sticky=E + W + N + S)
        dataTableFrame.grid_rowconfigure(0, weight=1)
        dataTableFrame.grid_columnconfigure(0, weight=2)

        # -----------------------------------------------------------------------------------------------------------------------------
        # Frame for data
        allDataFrame = LabelFrame(master, text="Data Preparation", background="gray69")
        allDataFrame.grid(row=1, column=0, padx=3, pady=3, sticky=E + W + N + S)
        allDataFrame.rowconfigure(0, weight=1)
        allDataFrame.columnconfigure(0, weight=2)
        allDataFrame.rowconfigure(0, weight=1)
        allDataFrame.columnconfigure(1, weight=3)

        # Frame for buttons to prepare data
        dataFrame = LabelFrame(allDataFrame, text="Attributes", background="gray69")
        dataFrame.grid(row=0, column=0, padx=3, pady=3, sticky="nsew")
        dataFrame.grid_rowconfigure(0, weight=1)
        dataFrame.grid_columnconfigure(0, weight=2)

        # Frame to see data
        viewDataFrame = LabelFrame(allDataFrame, text="Selected Attributes", background="gray69")
        viewDataFrame.grid(row=0, column=1, padx=3, pady=3, sticky="nsew")
        viewDataFrame.grid_rowconfigure(0, weight=1)
        viewDataFrame.grid_columnconfigure(0, weight=3)
        viewDataFrame.grid_rowconfigure(1, weight=1)
        viewDataFrame.grid_columnconfigure(0, weight=1)
        viewDataFrame.grid_rowconfigure(1, weight=1)
        viewDataFrame.grid_columnconfigure(2, weight=1)

        # -----------------------------------------------------------------------------------------------------------------------------

        # Frame for statistics of file
        statisticsFrame = LabelFrame(master, text="Functions", background="gray69")
        statisticsFrame.grid(row=2, column=0, padx=3, pady=3, sticky=E + W + N + S)
        statisticsFrame.grid_rowconfigure(0, weight=1)
        statisticsFrame.grid_columnconfigure(0, weight=1)
        statisticsFrame.grid_columnconfigure(1, weight=1)
        statisticsFrame.grid_columnconfigure(2, weight=1)

        # Frame for NULL values
        nullFrame = LabelFrame(statisticsFrame, text="NULL Values", background="gray69")
        nullFrame.grid(row=0, column=0, padx=3, pady=3, sticky=E + W + N + S)
        nullFrame.grid_rowconfigure(0, weight=1)
        nullFrame.grid_columnconfigure(0, weight=1)
        nullFrame.grid_columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------------------------------------

        # Frame for data table
        # self.tableFrame = LabelFrame(allDataFrame, text="Table", width=500, background="gray69", highlightcolor="red", highlightbackground="blue", highlightthickness=3)

        self.removeLinesFrame = LabelFrame(statisticsFrame, text="Remove Lines", background="gray69")
        self.removeLinesFrame.grid(row=0, column=2, padx=3, pady=3, sticky=E + W + N + S)
        self.removeLinesFrame.grid_rowconfigure(0, weight=1)
        self.removeLinesFrame.grid_columnconfigure(0, weight=1)
        self.removeLinesFrame.grid_columnconfigure(1, weight=1)
        self.removeLinesFrame.grid_columnconfigure(2, weight=1)
        self.removeLinesFrame.grid_columnconfigure(3, weight=1)

        # -------------------------------------------------- OPEN FILE ---------------------------------------------------------------------------
        # Name of File
        self.fileNameEntry = Label(fileNameFrame)
        self.fileNameEntry.config(state="disabled")
        self.fileNameEntry.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        # self.fileNameEntry.rowconfigure(0, weight=1)
        # self.fileNameEntry.columnconfigure(0, weight=1)

        # Visualize Data On Table
        # View data in table
        self.showData = Button(dataTableFrame, text="View Data in Table", command=self.showDataInTable)
        self.showData.config(state="disabled")
        self.showData.grid(row=0, column=0, padx=3, pady=3, sticky=E + W + N + S)
        # self.showData.rowconfigure(0, weight=1)
        # self.showData.columnconfigure(0, weight=1)

        # -----------------------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------- DATA AND STATISTICS OF COLUMNS --------------------------------------------------------------------------
        # List of Columns
        self.lb_colunas = Listbox(dataFrame, selectmode='multiple')
        self.lb_colunas.grid(row=0, column=0, padx=3, pady=3, sticky=E + W + N + S)
        self.lb_colunas.rowconfigure(0, weight=1)
        self.lb_colunas.columnconfigure(0, weight=1)

        # Remove Column
        self.removeColumn = Button(dataFrame, text="Remove Column", command=self.removeMultipleColumns)
        self.removeColumn.config(state="disabled")
        self.removeColumn.grid(row=1, column=0, padx=3, pady=3, sticky=E + W + N + S)
        self.removeColumn.rowconfigure(0, weight=1)
        self.removeColumn.columnconfigure(0, weight=1)

        # Rename Column
        self.renameColumn = Button(dataFrame, text="Rename Column", command=self.renameColumns)
        self.renameColumn.config(state="disabled")
        self.renameColumn.grid(row=2, column=0, padx=3, pady=3, sticky=E + W + N + S)
        self.renameColumn.rowconfigure(0, weight=1)
        self.renameColumn.columnconfigure(0, weight=1)

        # save target column
        self.targetCol = Button(dataFrame, text="Save target column", command=self.saveTargetColumn)
        self.targetCol.config(state="disabled")
        self.targetCol.grid(row=3, column=0, padx=3, pady=3, sticky=E + W + N + S)
        self.targetCol.rowconfigure(0, weight=1)
        self.targetCol.columnconfigure(0, weight=1)

        # Data of column
        self.data = Button(viewDataFrame, text="View Data Of Selected Column", command=self.printColumnData)
        self.data.config(state="disabled")
        self.data.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky=E + W + N + S)
        self.data.grid_rowconfigure(1, weight=1)
        self.data.grid_columnconfigure(0, weight=1)

        # Full statistics
        self.fullStatistics = Button(viewDataFrame, text="Calculate Statistics Of Selected Column",
                                     command=self.calculateStatistics)
        self.fullStatistics.config(state="disabled")
        self.fullStatistics.grid(row=1, column=2, columnspan=2, padx=3, pady=3, sticky=E + W + N + S)
        self.fullStatistics.grid_rowconfigure(1, weight=1)
        self.fullStatistics.grid_columnconfigure(2, weight=1)
        # -----------------------------------------------------------------------------------------------------------------------------

        # ---------------------------------------- FUNCTIONS FOR NULL VALUES -------------------------------------------------------------------------------------
        # Buttons for NULL Values -> MEAN

        self.values = StringVar(nullFrame)
        nullFunctions = ["Replace with Mean", "Replace with Median"]
        # Create variable to be the first selected function
        self.values.set(nullFunctions[0])

        self.dropdownNull = OptionMenu(nullFrame, self.values, *nullFunctions)
        # Create dropdown menu with line functions
        self.dropdownNull.config(font=('Helvetica', 8), state="disabled")
        self.dropdownNull.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownNull.grid_rowconfigure(0, weight=1)
        self.dropdownNull.grid_columnconfigure(0, weight=1)

        # Button to apply function for null values
        self.btn_applyReplace = Button(nullFrame, text="Apply", command=self.applyReplaceNullValues)
        self.btn_applyReplace.config(state="disabled")
        self.btn_applyReplace.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)
        self.btn_applyReplace.grid_rowconfigure(0, weight=1)
        self.btn_applyReplace.grid_columnconfigure(1, weight=1)

        # -----------------------------------------------------------------------------------------------------------------------------

        # --------------------------------------- TEXT BOX --------------------------------------------------------------------------------------
        # TextBox to view data about columns
        self.txtData = Text(viewDataFrame)
        self.txtData.config(state="disabled")
        self.txtData.grid(row=0, column=0, columnspan=4, padx=3, pady=3, sticky=E + W + N + S)
        self.txtData.rowconfigure(0, weight=1)
        self.txtData.columnconfigure(0, weight=1)
        # -----------------------------------------------------------------------------------------------------------------------------

        # ---------------------------------------- ENCODING ---------------------------------------------------------------------------
        # Frame to Encoding
        encodingFrame = LabelFrame(statisticsFrame, text="Encoding", background="gray69")
        encodingFrame.grid(row=0, column=1, padx=3, pady=3, sticky=E + W + N + S)
        encodingFrame.grid_rowconfigure(0, weight=1)
        encodingFrame.grid_columnconfigure(0, weight=1)
        encodingFrame.grid_columnconfigure(1, weight=1)

        self.encodingValues = StringVar(encodingFrame)
        encondingFunctions = ["Ordinal Encoding", "Z-Score"]
        # Create variable to be the first selected function
        self.encodingValues.set(encondingFunctions[0])

        self.dropdownEncoding = OptionMenu(encodingFrame, self.encodingValues, *encondingFunctions)
        # Create dropdown menu with line functions
        self.dropdownEncoding.config(font=('Helvetica', 8), state="disabled")
        self.dropdownEncoding.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownEncoding.grid_rowconfigure(0, weight=1)
        self.dropdownEncoding.grid_columnconfigure(0, weight=1)

        # Button to apply function for null values
        self.btn_applyEncoding = Button(encodingFrame, text="Apply", command=self.applyEncoding)
        self.btn_applyEncoding.config(state="disabled")
        self.btn_applyEncoding.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)
        self.btn_applyEncoding.grid_rowconfigure(0, weight=1)
        self.btn_applyEncoding.grid_columnconfigure(1, weight=1)

        # ---------------------------------------- REMOVE LINES ---------------------------------------------------------------------------
        # List of Columns we can choose to remove specific lines
        self.columnsToRemove = StringVar(self.removeLinesFrame)
        self.columnsListLineToRemove = []

        self.dropdownColumns = OptionMenu(self.removeLinesFrame, NONE, NONE)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="disabled")
        self.dropdownColumns.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(0, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

        # List of Functions we can choose to remove specific lines
        self.variable = StringVar(self.removeLinesFrame)
        lineFunctions = ["Value less than", "Value bigger than", "Value equal to", "Null value"]
        # Create variable to be the first selected function
        self.variable.set(lineFunctions[0])

        self.dropdown = OptionMenu(self.removeLinesFrame, self.variable, *lineFunctions)
        # Create dropdown menu with line functions
        self.dropdown.config(font=('Helvetica', 8), state="disabled")
        self.dropdown.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdown.rowconfigure(0, weight=1)
        self.dropdown.columnconfigure(0, weight=1)

        # Input value for what lines will be removed
        self.inputValue = Entry(self.removeLinesFrame)
        self.inputValue.config(state="disabled")
        self.inputValue.grid(row=0, column=2, padx=3, pady=3, sticky=E + W + N + S)
        self.inputValue.rowconfigure(0, weight=1)
        self.inputValue.columnconfigure(0, weight=1)

        # Choose Lines To Remove Based On Values
        self.removeLines = Button(self.removeLinesFrame, text="Remove Lines", command=self.removeLinesByValues)
        self.removeLines.config(state="disabled")
        self.removeLines.grid(row=0, column=3, padx=3, pady=3, sticky=E + W + N + S)
        self.removeLines.rowconfigure(0, weight=1)
        self.removeLines.columnconfigure(0, weight=1)

        # --------------------------------------------------- LOGS ----------------------------------------------------------------------------
        # Log Frame
        logFrame = LabelFrame(master, text="Log", background="gray69")
        logFrame.grid(row=4, column=0, padx=3, pady=3, sticky=E + W + N + S)
        logFrame.grid_rowconfigure(0, weight=1)
        # logFrame.grid_columnconfigure(0, weight=1)
        logFrame.grid_columnconfigure(1, weight=1)

        # Buttons For Log Frame
        self.btn_log = Button(logFrame, text="Log", height=2, width=5, command=self.showLogCommands)
        self.btn_log.config(state="disabled")
        self.btn_log.grid(row=0, column=0, padx=3, pady=3, sticky=E + W + N + S)

        self.log_last_line = StringVar()
        self.label_log = Label(logFrame, width=200, height=2, textvariable=self.log_last_line)
        self.label_log.config(state="disabled")
        self.label_log.grid(row=0, column=1, columnspan=2, padx=3, pady=3)

        # TESTING
        # self.loadProject()

    def activateAllButtons(self):
        # Make all buttons usable
        self.fileNameEntry.config(state="normal")
        self.removeColumn.config(state="normal")
        self.targetCol.config(state="normal")
        self.showData.config(state="normal")
        self.data.config(state="normal")
        self.fullStatistics.config(state="normal")
        self.dropdownNull.config(state="normal")
        self.btn_applyReplace.config(state="normal")
        self.txtData.config(state="normal")
        self.dropdownEncoding.config(state="normal")
        self.btn_applyEncoding.config(state="normal")
        self.dropdownColumns.config(state="normal")
        self.dropdown.config(state="normal")
        self.inputValue.config(state="normal")
        self.removeLines.config(state="normal")
        self.btn_log.config(state="normal")
        self.label_log.config(state="normal")
        self.renameColumn.config(state="normal")

        # List of Columns we can choose to remove specific lines
        self.columnsToRemove = StringVar(self.removeLinesFrame)
        self.columnsListLineToRemove = []

        self.dropdownColumns = OptionMenu(self.removeLinesFrame, NONE, NONE)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="disabled")
        self.dropdownColumns.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(0, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

        columnsToRemove = self.table.getColumnNames()
        for col_name in columnsToRemove:
            self.columnsListLineToRemove.append(col_name)
        # Create variable to be the first selected function
        self.columnsToRemove.set(self.columnsListLineToRemove[0])

        self.dropdownColumns = OptionMenu(self.removeLinesFrame, self.columnsToRemove, *self.columnsListLineToRemove)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="normal")
        self.dropdownColumns.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(0, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

    # Open File and insert his name on Entry
    # OF
    def chooseNameOfProject(self):
        self.window = Toplevel()
        self.window.resizable(False, False)

        label = Label(self.window, text="Choose Name of Project")
        label.grid(row=0, column=0)

        self.projectNameEntry = Entry(self.window, width=100)
        self.projectNameEntry.grid(row=1, column=0)

        self.saveNameOfFile = Button(self.window, text="Save", command=self.openFile)
        self.saveNameOfFile.grid(row=2, column=0)

    def openFile(self):
        # Verify if name of project was chosen
        # Save name of project in a variable to destroy window
        self.projectName = self.projectNameEntry.get()
        if self.projectName == "":
            messagebox.showerror("Error", "Please select a name for the project")
            return
        path = Path(os.getcwd())
        parentPath = path.parent.absolute()
        for name in os.listdir(parentPath):
            if self.projectName == name:
                messagebox.showerror("Error", "Project name already exists")
                return
        # Close Window where we chose the name of the project
        self.window.destroy()

        # Open File
        self.filePath = filedialog.askopenfilename(initialdir="Documentos", title="Open File",
                                                   filetypes=(("CSV Files", "*.csv"),))

        if '|' in self.projectName:
            messagebox.showerror("Error", "Invalid project name. Can not contain caracter '|'")
        else:
            self.copiedFilePath = f"{parentPath}\\{self.projectName}\\DataFile{self.projectName}.csv"
            # create directory of project and subdirectories
            os.mkdir(f"..\\{self.projectName}")
            os.mkdir(f"..\\{self.projectName}\\Results")
            os.mkdir(f"..\\{self.projectName}\\Models")
            os.mkdir(f"..\\{self.projectName}\\Plots")

            self.sysLogFile = f"..\\{self.projectName}\\{self.projectName}syslog.txt"
            # ProjectPath
            projectPath = Path(self.copiedFilePath)
            self.projectPath = projectPath.parent.absolute()
            file = File.File()
            file.initDataFile(self.filePath, f"..\\{self.projectName}\\DataFile{self.projectName}.csv")
            self.projectDataLog = ProjectLogFile.ProjectLogFile(self.sysLogFile)
            self.table = Table.Table(file)

        self.activateAllButtons()

        # Insert name of file on Entry
        self.fileNameEntry.config(text=f"{self.filePath}")

        # for col_name in df.columns:
        #  lb_colunas.insert(END, col_name)

        # self.showDataInTable()
        self.log = LogFile.LogFile(self.projectPath)

        # write in the log file
        self.log.logActions(f"File: {self.filePath} opened")
        self.log.logActions(f"Project data file {self.copiedFilePath} created and opened")

        # write in the project data log file
        self.projectDataLog.writeLine(f"OF|{self.copiedFilePath}")

        # Show name of all columns
        self.printColumns()

        # Set FilePath and ProjectFolderPath
        self.classifySide.addFilePathProjectFolderPath(self.copiedFilePath, self.projectPath)

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # Close file

    # Rename Columns
    def renameColumns(self):
        window = Toplevel()
        window.resizable(False, False)

        renameColumn = Label(window, text="Choose a column of the list and rename it")
        renameColumn.grid(row=0, column=0)

        self.columns = StringVar(window)
        self.columnsList = []
        columns = self.table.getColumnNames()
        for col_name in columns:
            self.columnsList.append(col_name)

        # Create variable to be the first selected function
        self.columns.set(self.columnsList[0])

        self.dropdownColumns = OptionMenu(window, self.columns, *self.columnsList)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="normal")
        self.dropdownColumns.grid(row=1, column=0, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(1, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

        # New Column Name Entry
        self.newColumnName = Entry(window, width=100)
        self.newColumnName.grid(row=1, column=2, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)
        self.newColumnName.grid_rowconfigure(0, weight=1)
        self.newColumnName.grid_columnconfigure(0, weight=1)

        # Rename Column Button
        rename = Button(window, text="Rename Column", command=lambda: self.applyRenaming(window))
        rename.grid(row=2, column=1, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)
        rename.grid_columnconfigure(0, weight=1)
        rename.grid_rowconfigure(0, weight=1)

    def applyRenaming(self, window):
        # Get index of column which is going to be renamed
        indexColumn = self.columnsList.index(self.columns.get())

        # Verify if new name of column was written
        if self.newColumnName.get() != "":
            # Get new name of column
            newColumnName = self.newColumnName.get()
        else:
            messagebox.showerror("ERROR", "Please select a new name for the selected column")
            return

        # Rename name of column on file
        self.table.setValue(0, indexColumn, newColumnName)

        # Destroy window
        window.destroy()

        # Info about the renaming of column
        messagebox.showinfo("Column Renamed", f"Column was renamed to {newColumnName}")

        # Write on log.txt
        self.log.logActions(f"Column was renamed to {newColumnName}")

        # Re-Show name of all columns of the file
        self.printColumns()

        # Reescrever lista de colunas das linhas a remover
        columnsToRemove = self.table.getColumnNames()
        self.columnsListLineToRemove = []
        for col_name in columnsToRemove:
            self.columnsListLineToRemove.append(col_name)
        # Create variable to be the first selected function
        self.columnsToRemove.set(self.columnsListLineToRemove[0])

        self.dropdownColumns = OptionMenu(self.removeLinesFrame, self.columnsToRemove, *self.columnsListLineToRemove)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="normal")
        self.dropdownColumns.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(0, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

    # Romeve certain column
    def removeMultipleColumns(self):
        # Verify if any algorithm was selected
        if not self.lb_colunas.curselection():
            messagebox.showerror("Error", "Please select at least 1 column to remove")
            return
        else:
            pass

        # Get all selected columns indexes
        clicked_columns = self.lb_colunas.curselection()

        strClickedColumns = ','.join(self.lb_colunas.get(i) for i in clicked_columns)

        indexToRemove = 0
        for columnToRemove in clicked_columns:
            column = columnToRemove - indexToRemove
            self.table.deleteColumn(column)
            self.printColumns()
            # self.showDataInTable()
            indexToRemove = indexToRemove + 1

        # Info about removed columns
        messagebox.showinfo("Removed columns", f"Column(s) {strClickedColumns} were removed")

        # write in the log file
        self.log.logActions(f"Columns {strClickedColumns} removed")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # Reescrever lista de colunas das linhas a remover
        columnsToRemove = self.table.getColumnNames()
        self.columnsListLineToRemove = []
        for col_name in columnsToRemove:
            self.columnsListLineToRemove.append(col_name)
        # Create variable to be the first selected function
        self.columnsToRemove.set(self.columnsListLineToRemove[0])

        self.dropdownColumns = OptionMenu(self.removeLinesFrame, self.columnsToRemove, *self.columnsListLineToRemove)
        # Create dropdown menu with line functions
        self.dropdownColumns.config(font=('Helvetica', 8), state="normal")
        self.dropdownColumns.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.dropdownColumns.rowconfigure(0, weight=1)
        self.dropdownColumns.columnconfigure(0, weight=1)

        # write in the project data log file
        # self.projectDataLog.writeLine(f"DCS {strClickedColumns}")

    def removeLinesByValues(self):
        # Verificar se o nome da coluna inserida corresponde a alguma coluna de cima
        # Verificar o valor inserido que irá ser utilizado para fazer a remoçao
        # Ver as linhas cujos valores correspondem ao valor inserido
        # Eliminar essas linhas
        # Limpar todos os valores inseridos nos inputs
        # for line in range(1, self.table.dataFile.numOfLines):
        if self.variable.get() == 'Value less than':
            self.removeLineValueLowerThan(self.inputValue.get(),
                                          self.columnsListLineToRemove.index(self.columnsToRemove.get()))
        elif self.variable.get() == 'Value bigger than':
            self.removeLineValueBiggerThan(self.inputValue.get(),
                                           self.columnsListLineToRemove.index(self.columnsToRemove.get()))
        elif self.variable.get() == 'Value equal to':
            self.removeLineValueEqualTo(self.inputValue.get(),
                                        self.columnsListLineToRemove.index(self.columnsToRemove.get()))
        else:
            self.removeLineNullValue(self.columnsListLineToRemove.index(self.columnsToRemove.get()))

        # write in the project data log file
        #self.projectDataLog.writeLine("DLVE")

    def removeLineValueEqualTo(self, value, columnIndex):
        lines = self.table.dataFile.fileNumLines
        line_to_use = 1
        # FOR para percorrer as linhas
        for line in range(1, lines):
            error = float(self.table.getValue(line_to_use, columnIndex))

            # IF para verificar se o valor que está na coluna indicada é igual ao 'value' -> Utilizar o getValue() para fazer a comparacao
            if float(value) == error:
                line_to_remove = line_to_use
                # Se for, eliminar aquela linha
                self.table.deleteLine(line_to_remove)
            else:
                line_to_use = line_to_use + 1


        # Info about removed lines
        messagebox.showinfo("Removed lines",
                            f"Line(s) were removed where values are equal to {float(value)} in column {self.columnsToRemove.get()}")

        # write in the log file
        self.log.logActions(f"Lines with values equals to: {float(value)} in column: {self.columnsToRemove.get()} removed")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine(f"DLVE {value},{columnIndex}")

    def removeLineValueBiggerThan(self, value, columnIndex):
        lines = self.table.dataFile.fileNumLines
        line_to_use = 1
        # FOR para percorrer as linhas
        for line in range(1, lines):
            error = float(self.table.getValue(line_to_use, columnIndex))

            # IF para verificar se o valor que está na coluna indicada é maior que o 'value' -> Utilizar o getValue() para fazer a comparacao
            if float(value) < error:
                line_to_remove = line_to_use
                # Se for, eliminar aquela linha
                self.table.deleteLine(line_to_remove)
            else:
                line_to_use = line_to_use + 1

        # Info about removed lines
        messagebox.showinfo("Removed lines",
                            f"Line(s) were removed where values are bigger than {float(value)} in column {self.columnsToRemove.get()}")

        # write in the log file
        self.log.logActions(f"Lines with values greater than: {float(value)} in column: {self.columnsToRemove.get()} removed")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # # write in the project data log file
        # self.projectDataLog.writeLine(f"DLVG {value},{columnIndex}")

    def removeLineValueLowerThan(self, value, columnIndex):
        lines = self.table.dataFile.fileNumLines
        line_to_use = 1
        # FOR para percorrer as linhas
        for line in range(1, lines):
            error = float(self.table.getValue(line_to_use, columnIndex))

            # IF para verificar se o valor que está na coluna indicada é menor que o 'value' -> Utilizar o getValue() para fazer a comparacao
            if float(value) > error:
                line_to_remove = line_to_use
                # Se for, eliminar aquela linha
                self.table.deleteLine(line_to_remove)
            else:
                line_to_use = line_to_use + 1

        # Info about removed lines
        messagebox.showinfo("Removed lines",
                            f"Line(s) were removed where values are lower than {float(value)} in column {self.columnsToRemove.get()}")

        # write in the log file
        self.log.logActions(f"Lines with values lower than: {float(value)} in column: {self.columnsToRemove.get()} removed")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine(f"DLVL {value},{columnIndex}")

    def removeLineNullValue(self, columnIndex):
        lines = self.table.dataFile.fileNumLines
        line_to_use = 1

        # FOR para percorrer as linhas
        for line in range(1, lines):
            # IF para verificar se o valor que está na coluna indicada é null -> Utilizar o getValue() para fazer a comparacao
            if self.table.getValue(line_to_use, columnIndex) == '*':
                line_to_remove = line_to_use
                # Se for, eliminar aquela linha
                self.table.deleteLine(line_to_remove)
            else:
                line_to_use = line_to_use + 1
        # Se nao for, passar para a proxima linha
        # self.showDataInTable()

        # Show info about removed lines
        messagebox.showinfo("Removed Lines",
                            f"Line(s) were removed where values are null in column {self.columnsToRemove.get()}")

        self.table.dataFile.updateFile()

        # write in the log file
        self.log.logActions(f"Lines with null values removed")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine(f"DLNV {columnIndex}")

    # print column names in listbox
    def printColumns(self):
        self.lb_colunas.delete(0, END)
        colunas = self.table.getColumnNames()
        for col_name in colunas:
            self.lb_colunas.insert(END, col_name)
        # write in the log file

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()


    # print data of selected column in textbox
    def printColumnData(self):
        self.txtData.delete("1.0", END)
        self.txtData.insert(INSERT, "Column Data: " + self.lb_colunas.get(ACTIVE) + '\n\n')
        # All lines of column
        values = self.table.getColumn(self.lb_colunas.index(ACTIVE))
        numbers = 0
        strings = 0
        # loop for all lines of column
        for elem in range(1, len(values)):
            elem = values[elem]
            # convert item in float
            try:
                elem = float(elem)
                numbers += 1
            except:
                strings += 1

            if numbers > 0 and strings > 0:
                pass

        if numbers > 0 and strings > 0:
            self.txtData.insert(INSERT, "Data Types: Float and String \n")
        elif numbers > 0:
            self.txtData.insert(INSERT, "Data Types: Float \n")
        else:
            self.txtData.insert(INSERT, "Data Types: String \n")

        null_values = self.table.numOfLinesWithNullValues(self.lb_colunas.index(ACTIVE))
        if null_values > 0:
            self.txtData.insert(INSERT, "Null Values: There are lines with null values \n\n")
        else:
            self.txtData.insert(INSERT, "Null Values: There are no lines with null values \n\n")

        self.txtData.insert(INSERT, '\n\n')
        # write in the log file
        # self.log.logActions(f"Data of column {self.lb_colunas.get(ACTIVE)} shown in text box")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine("PCDT")

    # calculate statistics of each column
    def calculateStatistics(self):
        self.txtData.delete("1.0", END)
        self.txtData.insert(INSERT, "Statistics of Column: " + self.lb_colunas.get(ACTIVE) + '\n\n')
        # write in the log file
        self.log.logActions(f"Statistics of column {self.lb_colunas.get(ACTIVE)} calculated")

        # Calculate Statistics
        try:
            mean = "{:.2f}".format(self.table.calculateMean(self.lb_colunas.index(ACTIVE)))
            median = "{:.2f}".format(self.table.calculateMedian(self.lb_colunas.index(ACTIVE)))

            self.txtData.insert(INSERT, f"Mean = " + mean + "\n")
            self.txtData.insert(INSERT, f"Median = " + median + "\n")

            self.log.logActions(f"Mean = {mean}")
            self.log.logActions(f"Median = {median}")
        except:
            messagebox.showerror("Error",
                                 "Impossible to calculate mean and median because there are string values on specified column")

        try:
            min = self.table.calculateMin(self.lb_colunas.index(ACTIVE))
            max = self.table.calculateMax(self.lb_colunas.index(ACTIVE))

            self.txtData.insert(INSERT, f"Minimum = {min} \n")
            self.txtData.insert(INSERT, f"Maximum = {max} \n")

            self.log.logActions(f"Minimum = {min}")
            self.log.logActions(f"Maximum = {max}")
        except:
            messagebox.showerror("Error",
                                 "Impossible to calculate minimum and maximum value because there are no numerical values on specified column")

        num_lines = self.table.quantityOfValues()
        num_null_lines = self.table.numOfLinesWithNullValues(self.lb_colunas.index(ACTIVE))

        self.txtData.insert(INSERT, f"Number of lines = {num_lines} \n")
        self.txtData.insert(INSERT, f"Number of null lines = {num_null_lines}")
        self.txtData.insert(INSERT, '\n\n')

        self.log.logActions(f"Number of lines = {num_lines}")
        self.log.logActions(f"Number of null lines = {num_null_lines}")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine("CE")

    # Replace null values
    def applyReplaceNullValues(self):
        if self.values.get() == "Replace with Mean":
            self.replaceNullValuesWithMean()
        else:
            self.replaceNullValuesWithMedian()

    # replace null values with mean
    def replaceNullValuesWithMean(self):
        if not self.lb_colunas.index(ACTIVE):
            messagebox.showerror("Error", "Please select 1 column")
            return
        else:
            pass

        self.table.replaceNullValues(self.lb_colunas.index(ACTIVE),
                                     self.table.calculateMean(self.lb_colunas.index(ACTIVE)))
        #self.printColumnData()
        # self.showDataInTable()

        messagebox.showinfo("Replaced Null Values",
                            f"Replaced null values for column {self.lb_colunas.get(ACTIVE)} with mean")

        # write in the log file
        self.log.logActions(f"Null values of column {self.lb_colunas.get(ACTIVE)} replaced with mean")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine("NVRWM")

    # replace null values with medeian
    def replaceNullValuesWithMedian(self):
        if not self.lb_colunas.index(ACTIVE):
            messagebox.showerror("Error", "Please select 1 column")
            return
        else:
            pass

        self.table.replaceNullValues(self.lb_colunas.index(ACTIVE),
                                     self.table.calculateMedian(self.lb_colunas.index(ACTIVE)))
        #self.printColumnData()
        # self.showDataInTable()
        messagebox.showinfo("Replaced Null Values",
                            f"Replaced null values for {self.lb_colunas.get(ACTIVE)} with median")

        # write in the log file
        self.log.logActions(f"Null values of column {self.lb_colunas.get(ACTIVE)} replaced with median")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine("NVRWMD")

    def showDataInTable(self):
        # Create new Window
        top = Toplevel()
        top.resizable(True, True)

        # Create A Frame
        self.tableFrame = LabelFrame(top, text="Table", background="gray69")

        # Destroy everything inside of Frame
        for widget in self.tableFrame.winfo_children():
            widget.destroy()

        # Make frame appear in window
        self.tableFrame.pack(expand=1, fill="both")

        tv1 = ttk.Treeview(self.tableFrame)
        tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = Scrollbar(self.tableFrame, orient="vertical",
                                command=tv1.yview)  # command means update the yaxis view of the widget
        treescrollx = Scrollbar(self.tableFrame, orient="horizontal",
                                command=tv1.xview)  # command means update the xaxis view of the widget
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        tv1["column"] = list(self.table.getColumnNames())
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.column(column, anchor="center")
            tv1.heading(column, text=column)  # let the column heading = column name

        # Criar uma lista com os valores todos de uma linha
        lista_linha = []

        # Configurações para mudar a cor de fundo das linhas da treeview
        for line in range(1, self.table.dataFile.fileNumLines):
            for col in range(0, self.table.dataFile.fileNumColumns):
                value = self.table.getValue(line, col)
                lista_linha.append(value)
            # Inserir a linha completa na tabela
            tv1.insert('', 'end',
                       values=lista_linha)  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
            # Limpar a linha para ser possivel gerar a proxima
            lista_linha.clear()
            if line == 2000:
                break

    # save data do file
    def saveValuesToFile(self):
        self.table.dataFile.writeContentsOfWriteBuffer()
        # write in the log file
        self.log.logActions(f"Data saved to the copy of the original file")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # write in the project data log file
        # self.projectDataLog.writeLine("SVF")

    def editarFicheiro(self):
        for col in range(0, self.table.dataFile.fileNumColumns):
            if col < self.table.dataFile.fileNumColumns:
                widget = self.tableFrame.grid_slaves(row=1, column=col)[0]
                self.table.setValue(0, col, widget.get())
        self.printColumns()
        self.table.dataFile.updateFile()

    def saveTargetColumn(self):
        if not self.lb_colunas.index(ACTIVE):
            messagebox.showerror("Error", "Please select 1 column")
            return
        else:
            pass

        # Get selected column and save as Target Column
        self.targetColumm = self.lb_colunas.get(ACTIVE)
        self.target_column_index = self.lb_colunas.index(ACTIVE)
        # Show info about saved target column
        messagebox.showinfo(title="Target Column", message=f"Target column: {self.targetColumm}")

        # write in the log file
        self.log.logActions(f"Column {self.lb_colunas.get(ACTIVE)} saved as target column")

        # write in the project data log file
        self.projectDataLog.writeLine(f"STC|{self.targetColumm}|{self.target_column_index}")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # Set target column for CLASSIFY
        self.classifySide.setTargetColumn(self.targetColumm, self.target_column_index)

    def preprocessingTasks(self):
        oc = pp.OrdinalEncoder()

    def applyEncoding(self):
        if self.encodingValues.get() == "Ordinal Encoding":
            self.ordinalEncoding()  # Mas esta funcao precisa de receber a coluna ou nao?
            # Caso seja preciso, tens aqui a coluna ativa " self.lb_colunas.get(ACTIVE) "
        elif self.encodingValues.get() == "One-Hot Encoding":
            self.oneHotEncoding()  # Mas esta funcao precisa de receber a coluna ou nao?
            # Caso seja preciso, tens aqui a coluna ativa " self.lb_colunas.get(ACTIVE) "
        else:
            if not self.targetColumm:
                messagebox.showerror("Error", "Select target column first")
                return
            else:
                self.z_score(self.targetColumm)  # Mas esta funcao precisa de receber a coluna ou nao?
            # Caso seja preciso, tens aqui a coluna ativa " self.lb_colunas.get(ACTIVE) "

    # Function which aplies ORDINAL ENCODING
    def ordinalEncoding(self):
        self.table.ordinalEncoding(f"{self.copiedFilePath}")
        # self.showDataInTable()

        # Show info about ordinal encoding
        messagebox.showinfo("Ordinal Encoding", f"Ordinal Encoding used")

        # write in the log file
        self.log.logActions(f"Ordinal encoding aplied")

        # write in the project data log file
        #self.projectDataLog.writeLine("OE")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()
        # OHE

    # Function which aplies ONE-HOT ENCODING
    def oneHotEncoding(self):
        self.table.oneHotEncoding(f"{self.copiedFilePath}")
        # self.showDataInTable()

        # Show info about One Hot encoding
        messagebox.showinfo("One-Hot Encoding", f"One-Hot Encoding used")

        # write in the log file
        self.log.logActions(f"One Hot Encoding aplied")

        # write in the project data log file
        #self.projectDataLog.writeLine("OHE")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

        # ZS

    # Function which aplies Z-SCORE
    def z_score(self, columnIndex):
        self.table.dataFile.updateFile()
        self.table.z_score(f"{self.copiedFilePath}", columnIndex)
        # self.showDataInTable()

        # Show info about Z-Score encoding
        messagebox.showinfo("Z-Score", f"Z-Score used")

        # wirte in the log file
        self.log.logActions(f"Z-score normalizations aplied")

        # write in the project data log file
        #self.projectDataLog.writeLine("ZS")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

    # Function which load project
    def loadProject(self):
        sysLogFileName = filedialog.askopenfilename(initialdir="Documentos", title="Open File",
                                                    filetypes=(("Text Files", "*.txt"),))
        self.sysLogFile = ProjectLogFile.ProjectLogFile(sysLogFileName)
        self.sysLogFile.fileReference.seek(0, 0)
        while True:
            line = self.sysLogFile.fileReference.readline()
            if line == '':
                break
            splited = line.split('|')
            splited[1] = splited[1][:-1]
            if splited[0] == "OF":
                file = File.File()
                file.openDataFile(splited[1])
                self.copiedFilePath = splited[1]
                self.table = Table.Table(file)
                path = Path(sysLogFileName)
                self.projectPath = path.parent.absolute()
                self.log = LogFile.LogFile(self.projectPath)
                self.projectDataLog = ProjectLogFile.ProjectLogFile(sysLogFileName)
                self.printColumns()
            if splited[0] == "STC":
                self.targetColumm = splited[1]
                self.target_column_index = int(splited[2])
        # self.showDataInTable()

        # activate all buttons
        self.activateAllButtons()

        # self.classify.openFile(self.copiedFilePath)

        # Set FilePath and ProjectFolderPath For CLASSIFY.
        self.classifySide.addFilePathProjectFolderPath(self.copiedFilePath, self.projectPath)
        # Set target column for CLASSIFY
        self.classifySide.setTargetColumn(self.targetColumm, self.target_column_index)

        # Insert name of file on Entry
        self.fileNameEntry.config(text=f"{self.copiedFilePath}")

        # Apresentar a ultima linha do ficheiro log.txt na label
        self.showLastCommand()

    # Show log commands
    def showLogCommands(self):
        # Abrir o ficheiro log.txt para leitura
        # Criar uma nova janela
        # Colocar uma text box na nova janela
        # Copiar o texto do ficheiro log.txt para essa text box
        # Passar o estado da text box para disabled, de modo a que nao seja possivel escrever ou apagar
        # Fechar o ficheiro log.txt
        # ---------------------------------------------------------------------------------------------
        # Abrir o ficheiro log.txt para leitura
        logfile = open(f"{self.projectPath}\\log.txt", "r")

        # Criar uma nova janela
        window = Toplevel()
        window.resizable(True, True)

        # Colocar uma text box na nova janela
        textbox = Text(window)
        textbox.pack(fill=BOTH, expand=1, pady=10, padx=10)

        # Copiar o texto do ficheiro log.txt para essa text box
        textbox.insert(INSERT, logfile.read())

        # Passar o estado da text box para disabled
        textbox.config(state=DISABLED)

        # Fechar o ficheiro log.txt
        logfile.close()

    # Show on label the last log command
    def showLastCommand(self):
        # Abrir o ficheiro log.txt para leitura
        # Ler a ultima linha do ficheiro log.txt
        # Colocar a ultima linha na label ao lado do botao de LOG
        # Fechar o ficheiro log.txt
        # -------------------------------------------------------------------------------
        # Abrir o ficheiro log.txt para leitura
        logfile = open(f"{self.projectPath}\\log.txt", "r")

        # Ler a ultima linha do ficheiro log.txt
        lines = logfile.read().splitlines()
        last_line = lines[-1]

        # Colocar a ultima linha na label ao lado do botao de LOG
        self.log_last_line.set(last_line)

        # Fechar o ficheiro log.txt
        logfile.close()
