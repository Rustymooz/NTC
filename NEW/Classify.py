import multiprocessing
import threading
from datetime import datetime

import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, KFold, StratifiedShuffleSplit, StratifiedKFold, cross_validate
from sklearn import metrics
from sklearn.datasets import load_iris
import pandas
import numpy
import File
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Import to get all file names of Algorithms Folder
import os
from os import listdir
import importlib

from shutil import copyfile, copy2

# Import all Algorithms
# from Algorithms import *

# Descobrir o numero de parametros de uma funcao
from inspect import signature
from inspect import getfullargspec

from os.path import basename
import File
import LogFile
import ProjectLogFile
import sklearn.externals

import GUI
import sys

# IMPORT para abrir imagens
from PIL import Image


class Classify:
    def __init__(self, master):
        # self.filePath = "D:\\IPL\\4ano\\Projeto Informatico\\Projeto-Informatico_20_05_2021\\Projeto-Informatico_20_05_2021\\Projeto-Informatico\\ProjetoBom\\DataFileProjetoBom.csv"
        # self.filePath = "D:\\IPL\\4ano\\Projeto Informatico\\Projeto-Informatico_20_05_2021\\Projeto-Informatico_20_05_2021\\Projeto-Informatico\\ProjetoIntenso\\DataFileProjetoIntenso.csv"
        # FilePath of Modified File used in Data Preparation side
        # self.filePath = start.GUI.getFilePath(master)
        self.filePath = None
        self.data = [[]]
        self.rows = []
        self.target = []
        self.target_column_index = None
        self.target_column_name = None
        self.file = None
        # List of Chosen Algorithms
        self.listOfChosenAlgorithms = []
        self.log = None
        # Project Folder Path used in Data Preparation Side
        # self.projectFolderPath = f"{start.GUI.getProjectFilePath(master)}"
        self.projectFolderPath = None
        self.iris = load_iris()
        # self.openFile(self.filePath)
        # Variavel para garantir que os modulos sao importados apenas uma vez
        self.modulosJaImportados = 0
        # Dicionario dos algoritmos e instancias a importar => <Nome do Algoritmo> : <Modulo.Funcao do Algoritmo>
        self.dictInstanciasAlgoritmos = {}
        # Dicionario dos algoritmos e funcoes a importar
        self.dictAlgoritmos = {}
        # Variavel para garantir que o ficheiro só é aberto uma vez
        self.ficheiroFoiAberto = 0
        # Lista de algoritmos instanciados
        self.listOfInstantiatedAlgorithms = {}
        # Dicionario dos resultados obtidos de acordo com os algoritmos escolhidos
        self.dictResultados = {}
        # Caminho completo do modelo selecionado pelo utilizador
        self.fullpathSelectedModel = None
        # Variavel para a thread
        self.running_thread = None
        # Variavel para verificar se existe thread ativa ou nao
        self.isThreadUp = False
        # Booleano para controlar se o utilizar ja deu START e ainda está à espera que a classificação termine
        self.isClassifying = False

        # ---------------------------|
        # Visual of our Classify tab |
        # ---------------------------|

        # Para fazer com que os FRAMES aumentem caso haja espaço disponivel
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=8)
        master.grid_rowconfigure(0, weight=2)
        master.grid_rowconfigure(1, weight=3)
        master.grid_rowconfigure(2, weight=3)
        master.grid_rowconfigure(3, weight=3)
        master.grid_rowconfigure(4, weight=2)

        # Algorithms Frame
        algorithmsFrame = LabelFrame(master, text="Algorithms", background="gray69")
        algorithmsFrame.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky=E + W + N + S)
        algorithmsFrame.grid_columnconfigure(0, weight=1)

        # Frame para escolher algoritmos
        self.chooseAddAlgorithmFrane = Frame(algorithmsFrame, background="gray69")
        self.chooseAddAlgorithmFrane.grid(row=0, column=0, pady=3)

        # Show List of All Algorithms of the Project
        self.varOflistOfAlgorithms = StringVar(self.chooseAddAlgorithmFrane)

        # Get all algorithms of the project
        self.listOfAlgorithms = []

        # Get all files of directory "Algorithms"
        entries = os.listdir('Algorithms')
        for entry in entries:
            # Para retirar o __py__cache
            if entry.endswith(".py"):
                # Append all filenames to the listOfAlgorithms
                self.listOfAlgorithms.append(os.path.splitext(entry)[0])

        # Create variable to be the first selected function
        self.varOflistOfAlgorithms.set(self.listOfAlgorithms[0])

        # Create dropdown where all algorithms will be placed
        self.dropdownAlgorithms = OptionMenu(self.chooseAddAlgorithmFrane, self.varOflistOfAlgorithms,
                                             *self.listOfAlgorithms)
        # Create dropdown menu with line functions
        self.dropdownAlgorithms.config(font=('Helvetica', 8), state="disabled")
        self.dropdownAlgorithms.grid(row=0, column=0, columnspan=3, pady=3, padx=3)
        self.dropdownAlgorithms.grid_rowconfigure(0, weight=1)
        self.dropdownAlgorithms.grid_columnconfigure(0, weight=1)

        # Button to choose algorithms
        self.chooseAlgorithm = Button(self.chooseAddAlgorithmFrane, text="Choose Algorithms",
                                      command=self.chosenAlgorithms)
        self.chooseAlgorithm.config(state="disabled")
        self.chooseAlgorithm.grid(row=0, column=3, padx=3, pady=3)

        # Frame para adicionar um novo algoritmo ao programa
        addAlgorithmFrame = LabelFrame(master, text="Add New Algorithm", background="gray69")
        addAlgorithmFrame.grid(row=0, column=3, pady=3, padx=3, sticky=E + W + N + S)
        addAlgorithmFrame.grid_columnconfigure(0, weight=1)
        addAlgorithmFrame.grid_rowconfigure(0, weight=1)

        # Button to Add Algorithms to the APP
        self.addAlgorithm = Button(addAlgorithmFrame, text="Add New Algorithm", command=self.addAlgorithms)
        self.addAlgorithm.config(state="disabled")
        self.addAlgorithm.grid(row=0, column=0, pady=20, padx=20, sticky=E + W + N + S)
        '''
        # Button to Add New Algorithm to the APP
        # Creating a photoimage object to use image
        photo = PhotoImage(file="..\\Files\\icon.png")
        img_label = Label(algorithmsFrame, image=photo, width=100, height=100)
        img_label.grid(row=0, column=1)
        '''

        self.nameAlgorithmFrame = Frame(algorithmsFrame, background="gray69")
        self.nameAlgorithmFrame.grid(row=1, column=0, columnspan=3, pady=3, padx=3, sticky=E + W + N + S)
        self.nameAlgorithmFrame.grid_rowconfigure(0, weight=1)
        self.nameAlgorithmFrame.grid_columnconfigure(0, weight=1)

        # Label for all chosen algorithms
        self.nameAlgorithm = Label(self.nameAlgorithmFrame)
        self.nameAlgorithm.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky=E + W + N + S)
        self.nameAlgorithm.grid_columnconfigure(0, weight=1)

        # Clear list of chosen algorithms button
        self.clearListOfAlgorithmsButton = Button(self.nameAlgorithmFrame, text="Clear Chosen Algorithms",
                                                  command=self.cleanChosenAlgorithms)
        self.clearListOfAlgorithmsButton.config(state="disabled")
        self.clearListOfAlgorithmsButton.grid(row=0, column=3, padx=3, pady=3, sticky=E + W + N + S)

        # Train/Test Frame
        trainTestFrame = LabelFrame(master, text="Train Test", background="gray69")
        trainTestFrame.grid(row=1, column=0, columnspan=2, pady=3, padx=3, sticky=E + W + N)

        # Tkinter string variable
        # able to store any string value
        self.v = StringVar(master, "1")

        # Dictionary to create multiple buttons
        valuesTrainTest = {"Use Training Set": "1",
                           "Cross Validation": "2",
                           "Stratified K-Fold": "3",
                           "Percentage Split": "4",
                           "K-Fold": "5"
                           }

        # Variable to increment rows
        rowIndex = 0

        # Loop is used to create multiple Radiobuttons
        # rather than creating each button separately
        for (text, value) in valuesTrainTest.items():
            Radiobutton(trainTestFrame, text=text, variable=self.v,
                        value=value, command=self.activateEntry, background="gray69").grid(row=rowIndex, column=0,
                                                                                           columnspan=2, pady=3, padx=3,
                                                                                           sticky=W)
            rowIndex += 1

        # Entries for Train/Test
        self.crossValidationEntry = Entry(trainTestFrame)
        self.crossValidationEntry.grid(row=1, column=3, pady=3, padx=3, sticky=E)
        self.crossValidationEntry.configure(state="disabled")

        self.stratifiedKFoldEntry = Entry(trainTestFrame)
        self.stratifiedKFoldEntry.grid(row=2, column=3, pady=3, padx=3, sticky=E)
        self.stratifiedKFoldEntry.configure(state="disabled")

        self.percentageSplitEntry = Entry(trainTestFrame, state="disabled")
        self.percentageSplitEntry.grid(row=3, column=3, pady=3, padx=3, sticky=E)
        self.percentageSplitEntry.configure(state="disabled")

        self.trainValidationTestEntry = Entry(trainTestFrame, state="disabled")
        self.trainValidationTestEntry.grid(row=4, column=3, pady=3, padx=3, sticky=E)
        self.trainValidationTestEntry.configure(state="disabled")

        # Classification Algorithm Frame
        classificationFrame = LabelFrame(master, text="Classify", background="gray69")
        classificationFrame.grid(row=2, rowspan=2, column=0, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)
        # classificationFrame.grid_rowconfigure(0, weight=1)
        classificationFrame.grid_columnconfigure(0, weight=1)
        classificationFrame.grid_columnconfigure(1, weight=1)
        classificationFrame.grid_rowconfigure(1, weight=1)

        # Start Classification
        self.btnStart = Button(classificationFrame, text="Start", command=self.startWithThread)
        self.btnStart.config(state="disabled")
        self.btnStart.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)

        # Stop Classification
        self.btnStop = Button(classificationFrame, text="Stop", command=self.stop)
        self.btnStop.config(state="disabled")
        self.btnStop.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)

        # Output Frames
        self.outputFrame = LabelFrame(master, text="Output", background="gray69")
        self.outputFrame.grid(row=1, rowspan=5, column=2, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)

        # treinoLabel = Label(outputFrame, text="Ola")
        # treinoLabel.grid()

        # Notebook for TABS
        self.notebook = ttk.Notebook(self.outputFrame)
        # Place All Tabs on Screen
        self.notebook.pack(expand=1, fill="both")

        # Importar as instancias dos algoritmos da pasta Algorithms
        self.importAlgorithmsInstanceDynamically()

        # ListBox para todos as classifações feitas
        self.lb_resultados = Listbox(classificationFrame, selectmode="multiple")
        self.lb_resultados.grid(row=1, column=0, columnspan=2, padx=3, pady=3, sticky=E + W + N + S)
        self.lb_resultados.rowconfigure(1, weight=1)
        self.lb_resultados.columnconfigure(0, weight=1)

        # Botão para carregar os algortimos treinados
        self.btn_loadMetrics = Button(classificationFrame, text="Load Metrics", command=self.loadMetrics)
        self.btn_loadMetrics.grid(row=2, column=0, pady=3, padx=3, sticky=E + W + N + S)

        # Botão para remover os algortimos treinados
        self.btn_removeClassification = Button(classificationFrame, text="Remove Metrics", command=self.deleteMetrics)
        self.btn_removeClassification.grid(row=2, column=1, pady=3, padx=3, sticky=E + W + N + S)

        # --------------------------------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------- COMPARE RESULTS ------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------------------

        # Frame para comparar resultados
        self.compareResultsFrame = LabelFrame(master, text="Compare Results", background="gray69")
        self.compareResultsFrame.grid(row=5, column=0, pady=3, padx=3, sticky=E + W + N + S)
        self.compareResultsFrame.grid_columnconfigure(0, weight=1)
        self.compareResultsFrame.grid_rowconfigure(0, weight=1)

        # Botao para mostrar o resultado obtido
        self.btn_showResult = Button(self.compareResultsFrame, text="Compare", command=self.compareResults)
        self.btn_showResult.config(state="disabled")
        self.btn_showResult.grid(row=0, column=0, columnspan=2, padx=3, pady=3, sticky=E + W + N + S)

        # --------------------------------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------- SHOW GRAPHICS --------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------------------

        # Frame para visualizar graficos
        self.showPlotsFrame = LabelFrame(master, text="Visualize Plots", background="gray69")
        self.showPlotsFrame.grid(row=5, column=1, pady=3, padx=3, sticky=E + W + N + S)
        self.showPlotsFrame.grid_rowconfigure(0, weight=1)
        self.showPlotsFrame.grid_columnconfigure(0, weight=1)  # Fazer com que a dropdown cresca caso haja espaco
        self.showPlotsFrame.grid_columnconfigure(1, weight=1)  # Fazer com que o botao cresca caso haja espaco

        # Lista com os graficos que podem ser visualizados
        self.listOfPlots = StringVar(self.showPlotsFrame)
        self.listOfPlots.set("Confusion Matrix")  # Default Value

        # Criar a dropdown para escolher o grafico que se quer visualizar
        self.menuOfPlots = OptionMenu(self.showPlotsFrame, self.listOfPlots, "Confusion Matrix", "ROC Curve",
                                      "Precision Recall Curve")
        self.menuOfPlots.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)

        # Criar o botao para selecionar o grafico a visualizar
        self.showPlot = Button(self.showPlotsFrame, text="Show Plots", command=self.showPlots)
        self.showPlot.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)

        # --------------------------------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------- LOGS -----------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------------------
        # Log Frame
        logFrame = LabelFrame(master, text="Log", background="gray69")
        logFrame.grid(row=6, column=0, columnspan=4, padx=3, pady=3, sticky=E + W + N + S)
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

        # Criar Thread para ativar todos os botoes apos o utilizador selecionar um ficheiro
        thread = threading.Thread(target=self.activateButtons, args=())
        thread.daemon = True
        thread.start()

        # --------------------------------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------- MODELS ---------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------------------
        # Frame para carregar modelos e classificar com o modelo selecionado
        self.modelsFrame = LabelFrame(master, text="Models", background="gray69")
        self.modelsFrame.grid(row=4, column=0, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)
        self.modelsFrame.grid_rowconfigure(0, weight=1)
        self.modelsFrame.grid_rowconfigure(1, weight=1)
        self.modelsFrame.grid_columnconfigure(0, weight=1)
        self.modelsFrame.grid_columnconfigure(1, weight=1)

        # Botao para carregar modelos
        self.btn_loadModel = Button(self.modelsFrame, text="Load Model", command=self.loadModel)
        self.btn_loadModel.grid(row=0, column=0, pady=3, padx=3, sticky=E + W + N + S)

        # Botao para classificar com base no algoritmo selecionado
        self.btn_classifyWithModel = Button(self.modelsFrame, text="Classify", command=self.classifyWithExistentModel)
        self.btn_classifyWithModel.grid(row=0, column=1, pady=3, padx=3, sticky=E + W + N + S)

        # Label que mostra o modelo selecionado
        self.label_model = Label(self.modelsFrame)
        self.label_model.grid(row=1, column=0, columnspan=2, pady=3, padx=3, sticky=E + W + N + S)

        # --------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------- TABS ---------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------------------------------

        # Frame for

    # -----------------------------------------------------------------------------------------------------------------------------
    # ----------------  FUNCTIONS
    # -----------------------------------------------------------------------------------------------------------------------------

    # Activate All Buttons
    def activateButtons(self):
        # Enquanto o nome do ficheiro for NONE, damos return
        # Quando o nome do ficheiro se alterar, activamos os botoes
        # -----------------------------------------------------------------------------------------------------------------------
        # Enquanto o nome do ficheiro for NONE, damos return
        while self.filePath == None:
            pass

        # Quando o nome do ficheiro se alterar, activamos os botoes
        self.dropdownAlgorithms.config(state="normal")
        self.chooseAlgorithm.config(state="normal")
        self.addAlgorithm.config(state="normal")
        self.clearListOfAlgorithmsButton.config(state="normal")
        self.btnStart.config(state="normal")
        self.btnStop.config(state="normal")
        self.btn_showResult.config(state="normal")
        self.btn_log.config(state="normal")
        self.label_log.config(state="normal")

    # Activate Specific Entries for Classification
    def activateEntry(self):
        # Inactive all Entries
        if self.v.get() == "1":
            self.crossValidationEntry.configure(state='disabled')
            self.percentageSplitEntry.configure(state='disabled')
            self.stratifiedKFoldEntry.configure(state='disabled')
            self.trainValidationTestEntry.configure(state='disabled')

        # Activate CrossValidation Entry
        elif self.v.get() == "2":
            self.crossValidationEntry.configure(state='normal')
            self.percentageSplitEntry.configure(state='disabled')
            self.stratifiedKFoldEntry.configure(state='disabled')
            self.trainValidationTestEntry.configure(state='disabled')

        # Activate Stratified K-Fold Entry
        elif self.v.get() == "3":
            self.crossValidationEntry.configure(state='disabled')
            self.percentageSplitEntry.configure(state='disabled')
            self.stratifiedKFoldEntry.configure(state='normal')
            self.trainValidationTestEntry.configure(state='disabled')

        # Activate Percentage Split Entry
        elif self.v.get() == "4":
            self.crossValidationEntry.configure(state='disabled')
            self.percentageSplitEntry.configure(state='normal')
            self.stratifiedKFoldEntry.configure(state='disabled')
            self.trainValidationTestEntry.configure(state='disabled')

        # Activate Train-Validation-Test Entry
        else:
            self.crossValidationEntry.configure(state='disabled')
            self.percentageSplitEntry.configure(state='disabled')
            self.stratifiedKFoldEntry.configure(state='disabled')
            self.trainValidationTestEntry.configure(state='normal')

    def chosenAlgorithms(self):
        # Ver o algoritmo escolhido
        # Adicionar o algoritmo a uma lista com todos os algoritmos guardados
        self.listOfChosenAlgorithms.append(self.varOflistOfAlgorithms.get())

        # Guardar o nome do algoritmo
        self.varOflistOfAlgorithms.get()

        # Buscar o caminho da pasta dos algoritmos
        myPath = f"Algorithms"
        # PARA TODOS OS ALGORITMOS DA PASTA ALGORITMOS
        for algoritmo in listdir(myPath):
            algoritmoSemExtensao = os.path.splitext(algoritmo)[0]
            # Verificar se o algoritmo escolhido é igual a um dos algoritmos daquela diretoria
            if self.varOflistOfAlgorithms.get() == algoritmoSemExtensao:
                # Criar uma signature
                sig = signature(self.dictInstanciasAlgoritmos[self.varOflistOfAlgorithms.get()])
                # Descobrir o numero de parametros que a funcao precisa
                params = sig.parameters
                lig = getfullargspec(self.dictInstanciasAlgoritmos[self.varOflistOfAlgorithms.get()])
                # Caso o construtor do algoritmo escolhido tenha atributos
                if len(params) > 0:
                    # Variavel para contar quantas entries vao ser criadas
                    countEntries = 0

                    # Criar uma window que passe os valores necessarios ao algoritmo escolhido
                    self.window = Toplevel()
                    self.window.resizable(False, False)

                    # Criar uma lista de parametros vazia que vai guardar todos os parametros inseridos pelo utilizador
                    self.listOfFunctionParameters = []

                    # Linhas onde os inputs vao ficar
                    rows = 0

                    # Criar os inputs dinamicamente para os valores pedidos pelo algoritmo
                    for parametro in params:
                        if countEntries < len(params):
                            # Criar label para dizer o que o user tem de selecionar
                            label = Label(self.window, text=f"{parametro}: ")
                            label.grid(row=rows, column=0, pady=3, padx=3)

                            # Criar o input
                            entry = Entry(self.window)
                            entry.grid(row=rows, column=1, pady=3, padx=3)

                            # Aumentar a variavel que dita em que linha os inputs vao ser apresentados
                            rows += 1
                            self.listOfFunctionParameters.append(entry)
                            countEntries += 1

                        # Mostrar o parametro selecionado

                    finish = Button(self.window, text="Finish", command=lambda: self.instantiateAlgorithm(
                        self.dictInstanciasAlgoritmos[self.varOflistOfAlgorithms.get()]))
                    finish.grid(row=rows, column=0)

                else:
                    self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[self.varOflistOfAlgorithms.get()]] = \
                    self.dictInstanciasAlgoritmos[self.varOflistOfAlgorithms.get()]

                '''
                if algoritmoSemExtensao == "KNN":
                    # Criar uma window que passe os valores necessários ao algoritmo escolhido
                    self.window = Toplevel()
                    self.window.resizable(False, False)

                    self.neigbhoors = Entry(self.window)
                    self.neigbhoors.pack(side=LEFT)

                    finish = Button(self.window, text="Finish", command=lambda: self.instantiateAlgorithm(self.neigbhoors.get()))
                    finish.pack(side=RIGHT)
                else:
                    pass
                '''
            else:
                # Aceder ao algoritmo utilizado dinamicamente
                pass

        # Lista de algoritmos sem as plicas
        without_single_quotes = "[{0}]".format(', '.join(map(str, self.listOfChosenAlgorithms)))

        # Adicionar os algoritmos selecionados à label abaixo
        self.nameAlgorithm = Label(self.nameAlgorithmFrame, text=f"{without_single_quotes[1:-1]}")
        self.nameAlgorithm.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky=E + W + N + S)
        self.nameAlgorithm.grid_columnconfigure(0, weight=1)

    def instantiateAlgorithm(self, algoritmo):
        for item in self.listOfFunctionParameters:
            # Criar uma instancia daquele algoritmo
            self.listOfInstantiatedAlgorithms[algoritmo] = algoritmo(item.get())
        self.window.destroy()

    def cleanChosenAlgorithms(self):
        # for algoritmos in self.listOfAlgorithms:
        self.listOfChosenAlgorithms = []

        # Limpar a label que tem a lista de algoritmos selecionados
        self.nameAlgorithm = Label(self.nameAlgorithmFrame, text="")
        self.nameAlgorithm.grid(row=0, column=0, columnspan=3, padx=3, pady=3, sticky=E + W + N + S)
        self.nameAlgorithm.grid_columnconfigure(0, weight=1)

    # falta conseguir criar um array 2d com os valores das celulas da tabela, tirando a coluna target,
    # que tem de ficar a parte

    def openFile(self, filePath):
        targetColumn = []
        self.file = File.File()
        self.file.openDataFile(filePath)
        self.log = LogFile.LogFile(self.projectFolderPath)
        # column_name_line = self.file.getLine(0)
        for i in range(1, self.file.fileNumLines):
            # columns = self.file.getLine(i)
            line = self.file.getLine(i)
            targetColumn = numpy.append(targetColumn, line.pop(self.target_column_index))
            self.rows = numpy.append(self.rows, line)
            # self.data = numpy.append(self.data, self.file.getLine(i))
        self.rows = numpy.reshape(self.rows, (self.file.fileNumLines - 1, self.file.fileNumColumns - 1))
        self.target = targetColumn

    # Function which add tabs according to the number of chosen algorithms
    def addTabs(self, algorithm, configs, resultado):
        # Get current timestamp para meter no nome do ficheiro das metricas e para apresentar na listbox
        # now = datetime.now()
        current_timestamp = resultado[1]  # now.strftime("%d_%m_%Y_%H_%M_%S")
        # separar timestamp
        data = current_timestamp.split("_", 3)
        dataFinal = data[0] + "-" + data[1] + "-" + data[2]
        horario = data[3].replace("_", ":")
        timestamp = dataFinal + " " + horario

        current_timestamp_listbox = timestamp

        # Tabs For Results
        # Creation of the space where we all tabs will be placed
        self.tab = Frame(self.notebook)
        self.notebook.add(self.tab, text=f"{current_timestamp_listbox} - {algorithm}")

        # Add information to the TAB
        # Create Text Box
        results = Text(self.tab)
        results.pack(expand=1, fill="both")


        # Criar um ficheiro que vai guardar todas as configurações relacionadas ao algoritmo utilizado
        config_results_file = open(f"{self.projectFolderPath}\\Results\\Metrics_{current_timestamp}_{algorithm}.txt",
                                   "a")

        # Linha para dizer que aqui vao ficar as configuracoes escolhidas pelo utilizador
        results.insert(INSERT, "Configurações: \n")
        # Escrever no ficheiro que guarda as configurações
        config_results_file.write("Configurações: \n")

        # Lista de configuracoes a serem apresentadas na text box e escritas no ficheiro
        for config in configs.keys():
            # Escrever na textBox a config
            results.insert(INSERT, config + ": ")
            results.insert(INSERT, configs[config])
            results.insert(INSERT, "\n")

            # Escrever no ficheiro a config
            config_results_file.write(config + ": ")
            config_results_file.write(str(configs[config]))
            config_results_file.write("\n")
        try:
            for parameter in resultado[2].keys():
                # Escrever linha na textBox
                results.insert(INSERT, parameter + ": ")
                results.insert(INSERT, resultado[2][parameter])
                results.insert(INSERT, "\n")

                # Escrever linha no ficheiro
                config_results_file.write(parameter + ": ")
                config_results_file.write(str(resultado[2][parameter]))
                config_results_file.write("\n")
        except:
            pass

        # Deixar uma linha em Branco Entre as configuracoes e o resultado do algoritmo
        results.insert(INSERT, "\n")
        # Deixar uma linha em Branco Entre as configuracoes e o resultado do algoritmo no ficheiro
        config_results_file.write("\n")

        # Linha para dizer que aqui vao ficar os resultados do algoritmo
        results.insert(INSERT, "Métricas: \n")
        # Escrever no ficheiro a indicacao das metricas obtidas
        config_results_file.write("Métricas: \n")


        # Metricas e resultados a serem apresentados na text box e escritas no ficheiro
        for item in resultado[0].keys():
            # Escrever linha na textBox
            results.insert(INSERT, item + ": ")
            results.insert(INSERT, resultado[0][item])
            results.insert(INSERT, "\n")

            # Escrever linha no ficheiro
            config_results_file.write(item + ": ")
            config_results_file.write(str(resultado[0][item]))
            config_results_file.write("\n")

        # Fechar o ficheiro que foi usado para guardar os resultados
        config_results_file.close()

        # Adicionar um key:value com os resultados
        self.dictResultados[f"{current_timestamp_listbox} - {algorithm}"] = config_results_file

        # Limpar a lista de resultados e reescrever a lista
        # Percorrer os resultados e inserir o nome da key na listbox
        self.lb_resultados.delete(0, END)
        for key_resultado in self.dictResultados.keys():
            # Inserir na listbox o value da key atual
            self.lb_resultados.insert(END, key_resultado)

        # Place All Tabs on Screen
        self.notebook.pack(expand=1, fill="both")

        # Classificação terminada com sucesso
        self.log.logActions("Classification ended with success")

    # Function which add algorithms to the project
    def addAlgorithms(self):
        # MessageBox which shows some alerts
        messagebox.showinfo("Add Algorithm Alerts", """ Addition of algorithms needs to follow some rules: 
                                                   \n\t 1. Name of function needs to be equal to the name the algorithm (It's case sensitive!)
                                                   \n\t 2. Code of the function needs to be similar to the code that will be presented next.
                                                   \n\t 3. File added needs to be .py.""")

        # Window with a template of how definition of function should be
        window = Toplevel()
        window.resizable(True, True)

        # Label With Some Infos
        lbInfos = Label(window, text="Here is an example of one algorithm thats exists on program."
                                     "Copy function above and make necessary changes to use your own algorithm.")
        lbInfos.pack(pady=10, padx=10)

        # TextBox With Template of Function
        txtBox = Text(window, height=10, width=10)

        # Function Presented as Template
        function = """import joblib

from sklearn.linear_model import LogisticRegression

from sklearn import metrics

# IMPORT do messagebox
from tkinter import messagebox

# IMPORT do timestamp
from datetime import datetime

# IMPORT para apresentar graficos
# É preciso instalar um package
import matplotlib.pyplot as plt
import scikitplot as skplt


# IMPORT para a janela que vai mostrar o grafico
from tkinter import *
from tkinter import ttk

# IMPORT para abrir imagens
from PIL import Image

class LR:
    def __init__(self):
        pass

    def LR(self, projectFolderPath, X_train, X_test, y_train, y_test):
        #X_train, X_test, y_train, y_test = train_test_split(rows, target, test_size=test_size)
        lr = LogisticRegression()

        # TRY
        # Fazer o fit
        try:
            lr.fit(X_train, y_train)
        # Abrir uma mensagem de erro a dizer que nao foi possivel fazer o fit
        except:
            messagebox.showerror("Error", "Verify number of classes of target column")
            return


        y_pred = lr.predict(X_test)

        # Get current timestamp
        now = datetime.now()
        current_timestamp = now.strftime("%d_%m_%Y_%H_%M_%S")
        # Create a file with model
        joblib.dump(lr, f'{projectFolderPath}\\Models\\LRmodel_{current_timestamp}.pkl')

        acc = metrics.accuracy_score(y_test, y_pred)
        f1 = metrics.f1_score(y_test, y_pred, average='macro')
        precision = metrics.precision_score(y_test, y_pred, average='macro')
        recall = metrics.recall_score(y_test, y_pred, average='macro')
        logLoss = metrics.log_loss(y_test, y_pred)
        rocAuc = metrics.roc_auc_score(y_test, y_pred, average='macro')
        confusionMatrix = metrics.confusion_matrix(y_test, y_pred)

        # Create dictionary with METRICS
        dictionary = {
            "Accuracy Score": "{0:.2f}".format(acc),
            "F1 Score": "{0:.2f}".format(f1),
            "Precision": "{0:.2f}".format(precision),
            "Recall": "{0:.2f}".format(recall),
            "Log Loss": "{0:.2f}".format(logLoss),
            "Roc AUC": "{0:.2f}".format(rocAuc),
            "Confusion Matrix": f"\n {confusionMatrix}"
        }

        #-----------------------------------------------------------------------------------------------------------
        # --------------------------------------------- GRAPHS -----------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------
        # Construir o grafico da metrica ROC Curve
        metrics.plot_roc_curve(lr, X_test, y_test)
        # Guardar o grafico
        plt.savefig(f'{projectFolderPath}\\Plots\\LRmodel_{current_timestamp}_ROCCurve.png')

        # Construir o grafico da CONFUSION MATRIX
        metrics.plot_confusion_matrix(lr, X_test, y_test)
        # Guardar o grafico
        plt.savefig(f'{projectFolderPath}\\Plots\\LRmodel_{current_timestamp}_ConfusionMatrix.png')

        # Construir o grafico da metrica PRECISION RECALL
        metrics.plot_precision_recall_curve(lr, X_test, y_test)
        plt.savefig(f'{projectFolderPath}\\Plots\\LRmodel_{current_timestamp}_PrecisionRecallCurve.png')


        return dictionary, current_timestamp
        # write in the log file
        # self.log.logActions(f"Logistic Regression aplied")

                    """

        # Show txtBox on Window
        txtBox.pack(expand=1, fill="both", padx=10, pady=10)

        # Insert function on txtBox
        txtBox.insert(END, function)

        # Button to add algorithm
        btnAddAlgorithm = Button(window, text="Add Algorithm", command=self.add)
        btnAddAlgorithm.pack(anchor="s", side=RIGHT, pady=10, padx=10)

    def addFilePathProjectFolderPath(self, filePath, projectFolderPath):
        self.filePath = filePath
        self.projectFolderPath = projectFolderPath
        # Quando o projeto for criado ou reaberto
        # o self.log vai ficar com o log.txt
        self.log = LogFile.LogFile(self.projectFolderPath)

    # Funcao para receber a target column e o index
    def setTargetColumn(self, targetColumm, target_column_index):
        self.target_column_name = targetColumm
        self.target_column_index = target_column_index

    def startWithThread(self):
        if self.target_column_index == None:
            messagebox.showerror("Error", "Choose target column first")
            return
        # Verificar se ja existe uma thread a correr
        if self.isClassifying == True:
            messagebox.showinfo("Classification in progress", "Classification in progress. \nWait until classification process terminates to start a new classification!")
            return
        else:
            # Variavel para controlar que a thread ja está a correr
            self.isClassifying = True

            # Variavel para depois matar a thread
            self.isThreadUp = True

            # Criar thread e iniciar a thread com a funcao START()
            self.running_thread = threading.Thread(target=self.start)
            self.running_thread.daemon = True
            self.running_thread.start()



    def start(self):
        if self.listOfChosenAlgorithms == []:
            messagebox.showerror("Error", "Choose at least one algorithm")
            return

            # Verificar se o ficheiro ja foi aberto
        if self.ficheiroFoiAberto == 0:
            try:
                # Open file to start playing with algorithms
                self.openFile(self.filePath)
            except:
                messagebox.showerror("Error", "Something went wrong when trying to classification")
                # Fechar o ficheiro
                self.file.close()

                # Retirar o self.rows e o self.target
                self.rows = []
                self.target = []

                self.isClassifying = False
                return

            # Alterar a variavel para mostrar que o ficheiro ja está aberto
            self.ficheiroFoiAberto = 1

        # Ver o dicionario com os algoritmos e respetivas funcoes

        # Classificar o dataset passando por todos os algoritmos selecionados pelo utilizador
        for alg in self.listOfChosenAlgorithms:
            # Chamar a funcao que lê o tipo de Train Test escolhido e corre a funcao correspondente aos algoritmos selecionados
            self.readTrainTestSplit(alg)

            # Verificar se o botao STOP foi clicado
            if self.isThreadUp == False:
                break

        # Fechar o ficheiro
        self.file.close()

        # Passar a variavel do self.ficheiroFoiAberto para 0
        self.ficheiroFoiAberto = 0

        # Retirar o self.rows e o self.target
        self.rows = []
        self.target = []

        # Booleano para dizer que a classificação terminou
        self.isClassifying = False


        # Apresentar mensagem a dizer que a classificação terminou
        # messagebox.showinfo("Classification Ended", "Classification of data with chosen algorithms has finished with success.")

    # Parar a classificação
    def stop(self):
        # Passar a variavel que garante que a classificação está a decorrer
        # para False
        self.isThreadUp = False

        # Avisar que a classificação foi parada
        messagebox.showinfo("Classification Stopped",
                            "Classification of data was stopped. You might wait until the last algorithm "
                            "finishes the classification.")

    #############################################################################
    ###########################  SPLIT DATA #####################################
    #############################################################################
    def allData(self, algoritmo):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.rows, self.target, random_state=0)

        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "Use Training Set",
            "Coluna Target": self.target_column_name  # self.target
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: Cross Validation")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            # Adicionar os resultados
            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("Error", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    def splitDataKFold(self, n_splits, algoritmo):
        kf = KFold(n_splits=n_splits)
        for train_index, test_index in kf.split(self.rows):
            self.X_train, self.X_test, self.y_train, self.y_test = self.rows[train_index], self.rows[test_index], \
                                                                   self.target[
                                                                       train_index], self.target[test_index]

        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "K-Fold",
            "Numero de Splits": n_splits,
            "Coluna Target": self.target_column_name  # self.target
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: K-Fold")
            self.log.logActions(f"Number Of Splits Used: {n_splits}")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            # self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](algoritmo, self.projectFolderPath,self.X_train, self.X_test, self.y_train, self.y_test))
            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("ERROR", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    def splitDataStratifiedSplit(self, n_splits, algoritmo):
        ss = StratifiedShuffleSplit(n_splits=n_splits)
        for train_index, test_index in ss.split(self.rows, self.target):
            self.X_train, self.X_test, self.y_train, self.y_test = self.rows[train_index], self.rows[test_index], \
                                                                   self.target[
                                                                       train_index], self.target[test_index]
        # self.trainKnn(X_train, X_test, y_train, y_test)
        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "Stratified Split",
            "Numero de Splits": n_splits,
            "Coluna Target": self.target_column_name  # self.target
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: Stratified Split")
            self.log.logActions(f"Number Of Splits Used: {n_splits}")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            # Adicionar resultados
            # self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](algoritmo, self.projectFolderPath, self.X_train, self.X_test, self.y_train, self.y_test))
            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("ERROR", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    def splitDataPercentage(self, test_size, algoritmo):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.rows, self.target,
                                                                                test_size=test_size)
        # self.addTabs("KNN Percentage", Algorithms.KNN.KNN.KNN(self.knnInstance, self.projectFolderPath, self.X_train, self.X_test,self.y_train, self.y_test))
        # self.trainKnn(X_train, X_test, y_train, y_test)

        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "Percentage Split",
            "Test Size": test_size,
            "Coluna Target": self.target_column_name
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: Percentage Split")
            self.log.logActions(f"Test Size Used: {test_size}")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            # Chamada à funcao que vai adicionar os resultados da classificacao do algoritmo às tabs
            # Recebe varios parametros
            # 1º => Nome do algoritmo
            # 2º => Lista de configuracoes utilizadas
            # 3º => Algoritmo escolhido pelo utilizador
            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("ERROR", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    def splitDataStratifiedKFold(self, n_splits, algoritmo):
        skf = StratifiedKFold(n_splits=n_splits)
        for train_index, test_index in skf.split(self.rows, self.target):
            self.X_train, self.X_test, self.y_train, self.y_test = self.rows[train_index], self.rows[test_index], \
                                                                   self.target[
                                                                       train_index], self.target[test_index]

        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "Stratified K-Fold",
            "Numero de Splits": n_splits,
            "Coluna Target": self.target_column_name  # self.target
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: Stratified K-Fold")
            self.log.logActions(f"Number Of Splits Used: {n_splits}")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            # self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](algoritmo, self.projectFolderPath, self.X_train, self.X_test, self.y_train, self.y_test))
            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("ERROR", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    # Cross Validation
    def crossValidation(self, test_size, algoritmo):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.rows, self.target,
                                                                                test_size=test_size, random_state=0)

        dictionary = {
            "Algoritmo Utilizado": algoritmo,
            "Método de Divisão de Dados Utilizado": "Cross Validation",
            "Test Size": test_size,
            "Coluna Target": self.target_column_name  # self.target
        }

        try:
            # Inserir linhas no ficheiro de log
            self.log.logActions(f"Classification started!")
            self.log.logActions(f"Used Algorithm: {algoritmo}")
            self.log.logActions(f"Division Method Used: Cross Validation")
            self.log.logActions(f"Test Size Used: {test_size}")
            self.log.logActions(f"Column Target Used: {self.target_column_name}")
            self.log.logActions("Classification in progress...")

            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

            self.addTabs(f"{algoritmo}", dictionary, self.dictAlgoritmos[algoritmo](
                self.listOfInstantiatedAlgorithms[self.dictInstanciasAlgoritmos[algoritmo]], self.projectFolderPath,
                self.X_train, self.X_test, self.y_train, self.y_test))


            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

        except:
            messagebox.showerror("ERROR", "Something went wrong with classification")
            self.log.logActions("Error occurred during classification. Classification terminated.")
            # Apresentar a ultima linha do log.txt na label
            self.showLastCommand()

    # Activate Specific Entries for Classification
    def readTrainTestSplit(self, algoritmo):
        # Classificar o dataset com todos os dados
        if self.v.get() == "1":
            try:
                self.allData(algoritmo)
            except:
                messagebox.showerror("ERROR", "Something went wrong!")

        # Activate CrossValidation Entry
        elif self.v.get() == "2":
            try:
                test_size = float(self.crossValidationEntry.get())
                self.crossValidation(test_size, algoritmo)
            except:
                messagebox.showerror("ERROR", "Specify how you want to divide data. Use percentual values")

        # Activate Stratified K-Fold Entry
        elif self.v.get() == "3":
            try:
                split = int(self.stratifiedKFoldEntry.get())
                self.splitDataStratifiedKFold(split, algoritmo)
            except:
                messagebox.showerror("ERROR", "Specify how you want to divide data. Use integer values")

        # Activate Percentage Split Entry
        elif self.v.get() == "4":
            try:
                testSize = float(self.percentageSplitEntry.get())
                self.splitDataPercentage(testSize, algoritmo)
            except:
                messagebox.showerror("ERROR", "Specify how you want to divide data. Use percentual values")

        # Activate Train-Validation-Test Entry
        else:
            try:
                # Para ja está a utilizar o Data K Fold
                n_splits = int(self.trainValidationTestEntry.get())
                self.splitDataKFold(n_splits, algoritmo)
            except:
                messagebox.showerror("ERROR", "Specify how you want to divide data. Use integer values")

    def importAlgorithmsInstanceDynamically(self):
        # Importar os modulos apenas na primeira vez que clicamos no botao START
        if self.modulosJaImportados == 0:
            # Passar a variavel que garante que os modulos ja foram importados para 1 para que nao voltem a ser importados
            self.modulosJaImportados = 1
            # Importar todos os modulos e funcoes existentes na pasta Algorithms
            # Lista de todos os algoritmos para dar import
            listOfAlgorithmsToImport = []

            # Dicionario dos algoritmos e funcoes a importar => <Nome do Algoritmo> : <Modulo.Funcao do Algoritmo>
            # self.dictAlgoritmos = {}

            # Caminho da pasta onde estao todos os algoritmos
            myPath = f"Algorithms"

            # Limpar cache por causa dos imports dinamicos
            importlib.invalidate_caches()

            # PARA TODOS OS ALGORITMOS DA PASTA ALGORITMOS
            for algoritmo in listdir(myPath):
                # Caso o ficheiro encontrado na pasta dos Algorithms acabe em '.py'
                if algoritmo.endswith(".py"):
                    # Retirar o '.py' do ficheiro do algoritmo
                    algoritmoSemExtensao = os.path.splitext(algoritmo)[0]
                    # Adicionar o algoritmo à listOfAlgorithmsToImport
                    listOfAlgorithmsToImport.append(algoritmoSemExtensao)
                    # Importar o modulo correspondente ao algoritmo encontrado
                    module = importlib.import_module("Algorithms." + str(algoritmoSemExtensao))
                    # Adicionar ao dicionario o nome do algoritmo e a instancia correspondente a esse algoritmo
                    # 'algoritmoSemExtensao' : Algorithms.algoritmoSemExtensao.algoritmoSemExtensao
                    self.dictInstanciasAlgoritmos[algoritmoSemExtensao] = getattr(module, algoritmoSemExtensao)
                    # Adicionar ao dicionario o nome do algoritmo e a funcao correspondente a esse algoritmo
                    funcao = getattr(module, algoritmoSemExtensao)
                    self.dictAlgoritmos[algoritmoSemExtensao] = getattr(funcao, algoritmoSemExtensao)

    #############################################################################

    # Adicionar um novo algoritmo ao projeto
    def add(self):
        # Open FileDialog to choose algorithm to add
        addAlgorithmPY = filedialog.askopenfilename(initialdir="Documentos", title="Open File",
                                                    filetypes=(("PY Files", "*.py"),))

        # Adicionar um novo algoritmo ao projeto
        dir_name = 'Algorithms'

        # Nome do ficheiro adicionado sem o caminho completo
        filename = os.path.basename(addAlgorithmPY)

        for algoritmoNaPasta in listdir(dir_name):
            if algoritmoNaPasta == filename:
                messagebox.showerror("Invalid Algorithm", "There is a algorithm file with same name on program")
                return

        # Copiar o novo algoritmo para a pasta dos Algorithms
        copy2(addAlgorithmPY, dir_name)

        # Dar Import do novo algoritmo inserido
        # Caso o ficheiro encontrado na pasta dos Algorithms acabe em '.py'
        if addAlgorithmPY.endswith(".py"):
            # Retirar o '.py' do ficheiro do algoritmo
            algoritmoSemExtensao = os.path.splitext(filename)[0]
            # Importar o modulo correspondente ao algoritmo encontrado
            module = importlib.import_module("Algorithms." + str(algoritmoSemExtensao))
            # Adicionar ao dicionario o nome do algoritmo e a instancia correspondente a esse algoritmo
            # 'algoritmoSemExtensao' : Algorithms.algoritmoSemExtensao.algoritmoSemExtensao
            self.dictInstanciasAlgoritmos[algoritmoSemExtensao] = getattr(module, algoritmoSemExtensao)
            # Adicionar ao dicionario o nome do algoritmo e a funcao correspondente a esse algoritmo
            funcao = getattr(module, algoritmoSemExtensao)
            self.dictAlgoritmos[algoritmoSemExtensao] = getattr(funcao, algoritmoSemExtensao)

            # Reescrever a listBox dos algoritmos
            self.rewriteAlgorithmListBox()

            # Dizer que o algoritmo foi adicionado com sucesso
            messagebox.showinfo("Algorithm Added With Success",
                                f"Algorithm {algoritmoSemExtensao} added to the program with success")

            # Adicionar nova linha ao ficheiro de log
            # a dizer que o algoritmo foi inserio
            self.log.logActions(f"Algorithm {algoritmoSemExtensao} added to the program")

            # Reescrever a label do log com a nova linha de log
            self.showLastCommand()

    # Reescrever a lista de Algoritmos que se pode selecionar apos a insercao de um novo algoritmo
    def rewriteAlgorithmListBox(self):
        # Get all algorithms of the project
        self.listOfAlgorithms = []

        # Get all files of directory "Algorithms"
        entries = os.listdir('Algorithms')
        for entry in entries:
            # Para retirar o __py__cache
            if entry.endswith(".py"):
                # Append all filenames to the listOfAlgorithms
                self.listOfAlgorithms.append(os.path.splitext(entry)[0])

        # Create variable to be the first selected function
        self.varOflistOfAlgorithms.set(self.listOfAlgorithms[0])

        # Create dropdown where all algorithms will be placed
        self.dropdownAlgorithms = OptionMenu(self.chooseAddAlgorithmFrane, self.varOflistOfAlgorithms,
                                             *self.listOfAlgorithms)
        # Create dropdown menu with line functions
        self.dropdownAlgorithms.config(font=('Helvetica', 8), state="normal")
        self.dropdownAlgorithms.grid(row=0, column=0, columnspan=2, pady=3, padx=3)
        self.dropdownAlgorithms.grid_rowconfigure(0, weight=1)
        self.dropdownAlgorithms.grid_columnconfigure(0, weight=1)


    # Abrir uma janela com os resultados gravados
    def compareResults(self):
        # Verify if any algorithm was selected
        if not self.lb_resultados.curselection():
            messagebox.showerror("Error", "Please select at least 2 classifications from the list")
            return
        else:
            pass

        # Create new Window
        top = Toplevel()
        top.resizable(True, True)

        # Create A Frame
        tableFrame = LabelFrame(top, text="Table", background="gray69")

        # Destroy everything inside of Frame
        for widget in tableFrame.winfo_children():
            widget.destroy()

        # Make frame appear in window
        tableFrame.pack(expand=1, fill="both")

        tv1 = ttk.Treeview(tableFrame)
        tv1.place(relheight=1, relwidth=1)  # set the height and width of the widget to 100% of its container (frame1).

        treescrolly = Scrollbar(tableFrame, orient="vertical",
                                command=tv1.yview)  # command means update the yaxis view of the widget
        treescrollx = Scrollbar(tableFrame, orient="horizontal",
                                command=tv1.xview)  # command means update the xaxis view of the widget
        tv1.configure(xscrollcommand=treescrollx.set,
                      yscrollcommand=treescrolly.set)  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(side="bottom", fill="x")  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(side="right", fill="y")  # make the scrollbar fill the y axis of the Treeview widget

        lista_colunas = []
        lista_colunas.append("Métricas/Algoritmos")
        for item in self.lb_resultados.curselection():
            lista_colunas.append(self.lb_resultados.get(item))

        tv1["column"] = list(lista_colunas)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.column(column, anchor="center")
            tv1.heading(column, text=column)  # let the column heading = column name

        # Criar uma lista com os valores todos de uma linha
        metrica_acc = ["Accuracy-Score"]
        metrica_f1 = ["F1-Score"]
        metrica_precision = ["Precision"]
        metrica_recall = ["Recall"]
        metrica_log = ["Log-Loss"]
        metric_auc = ["ROC-AUC"]
        lista_metricas = []
        lista_metricas.append(metrica_acc)
        lista_metricas.append(metrica_f1)
        lista_metricas.append(metrica_precision)
        lista_metricas.append(metrica_recall)
        lista_metricas.append(metrica_log)
        lista_metricas.append(metric_auc)

        # Percorrer todos os items selecionados na listBox
        for item in self.lb_resultados.curselection():
            # Buscar o resultado selecionado da lista
            selectedResult = self.lb_resultados.get(item)
            # Fazer a divisao do resultado escolhido para conseguir ir buscar o ficheiro certo
            timestamp_data = selectedResult.split("-")
            timestamp_horario = selectedResult.split(":")
            # Descobrir o dia
            day = timestamp_data[0]
            # Descobrir o mes
            month = timestamp_data[1]
            # Descobrir o ano
            year = timestamp_data[2]
            year = year.split(" ")
            year = year[0]
            # Descobrir a hora
            hour = timestamp_horario[0]
            hour = hour.split(" ")
            hour = hour[1]
            # Descobrir o minuto
            minute = timestamp_horario[1]
            # Separar os segundos do algoritmo
            second = timestamp_horario[2]
            second = second.split(" - ")
            # Descobrir o algoritmo usado
            algoritmo = second[1]
            # Descobrir o segundo
            second = second[0]
            # Obter a data correta e conforme o ficheiro guardado
            selectedResult = f"{day}_{month}_{year}_{hour}_{minute}_{second}_{algoritmo}"
            # Abrir o ficheiro relacionado com o resultado obtido para leitura
            f = open(f"{self.projectFolderPath}\\Results\\Metrics_{selectedResult}.txt", "r")

            # Lista com todas as linhas
            all_lines = f.readlines()

            line_number = 0
            for line in all_lines:
                if line == '\n':
                    line_sem_valor = line_number
                    line_number += 1
                else:
                    line_number += 1

            # Configurações para mudar a cor de fundo das linhas da treeview
            for line in range(line_sem_valor + 2, len(all_lines)-3):
                result = all_lines[line].split(": ")
                lista_metricas[line - (line_sem_valor + 2)].append(result[1])

            f.close()

        for line in range(len(lista_metricas)):
            # Inserir a linha completa na tabela
            tv1.insert('','end',values=lista_metricas[line])  # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert

    # Show PLOTS
    def showPlots(self):
        # Garantir que está um algoritmo classificado da listbox selecionado
        # Buscar e guardar o grafico selecionado pelo utilizador
        # Buscar e guardar o algoritmo classificado presente na listbox
        # Procurar pelo grafico do algoritmo selecionado na pasta Plots
        # Apresentar o grafico encontrado numa nova janela
        # -----------------------------------------------------------------------
        # Garantir que está um algoritmo classificado da listbox selecionado
        selection = self.lb_resultados.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select one of the classified algorithms of the list on the left side")
            return
        else:
            # Buscar e guardar o grafico selecionado pelo utilizador
            selectedPlot = self.listOfPlots.get()
            # Remover os espaços que vêm da dropdown
            selectedPlot = selectedPlot.replace(" ", "")

            # Buscar e guardar o algoritmo classificado presente na listbox
            for item in selection:
                algorithm = self.lb_resultados.get(item)

                # Separar o resultado do item em várias partes para conseguir aceder ao grafico que se pretende
                timestamp = algorithm.split(" ")
                algorithm = timestamp[3]
                # Separar a data
                timestamp_data = timestamp[0]
                timestamp_data = timestamp_data.split("-")
                # Descobrir o dia
                day = timestamp_data[0]
                # Descobrir o mes
                month = timestamp_data[1]
                # Descobrir o ano
                year = timestamp_data[2]

                # Separar o horario
                timestamp_horario = timestamp[1]
                timestamp_horario = timestamp_horario.split(":")
                # Descobrir a hora
                hour = timestamp_horario[0]
                # Descobrir o minuto
                minute = timestamp_horario[1]
                # Descobrir o segundo
                second = timestamp_horario[2]

                # Timestamp completo do ficheio
                result = f"{day}_{month}_{year}_{hour}_{minute}_{second}"

                # Abrir o ficheiro com o grafico correspondente ao algoritmo escolhido
                plot_file = Image.open(f"{self.projectFolderPath}\\Plots\\{algorithm}model_{result}_{selectedPlot}.png")
                plot_file.show()

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
        logfile = open(f"{self.projectFolderPath}\\log.txt", "r")

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
        logfile = open(f"{self.projectFolderPath}\\log.txt", "r")

        # Ler a ultima linha do ficheiro log.txt
        lines = logfile.read().splitlines()
        last_line = lines[-1]

        # Colocar a ultima linha na label ao lado do botao de LOG
        self.log_last_line.set(last_line)

        # Fechar o ficheiro log.txt
        logfile.close()

    # Load Model Function
    def loadModel(self):
        model = filedialog.askopenfilename(initialdir=f"{self.projectFolderPath}", title="Choose Model", filetypes=(
            ("PKL Files", "*.pkl"),))
        modelName = os.path.basename(model)
        modelNameSemExtensao = os.path.splitext(modelName)[0]

        # Caminho completo do modelo selecionado
        self.fullpathSelectedModel = model

        # Apresentar o nome do modelo selecionado na label
        self.label_model["text"] = modelNameSemExtensao

        # Escrever no ficheiro de log a escolha do modelo
        self.log.logActions(f"Model {modelNameSemExtensao} loaded")

        self.showLastCommand()

    def classifyWithExistentModel(self):
        # Verificar se o utilizador ja escolheu um modelo
        if self.fullpathSelectedModel == None:
            messagebox.showerror("Error", "Choose model first")
            return
        else:
            pass

        if self.ficheiroFoiAberto == 0:
            # Open file to start playing with algorithms
            self.openFile(self.filePath)
            # Alterar a variavel para mostrar que o ficheiro ja está aberto
            self.ficheiroFoiAberto = 1
        else:
            pass


        modelName = os.path.basename(self.fullpathSelectedModel)
        modelNameSemExtensao = os.path.splitext(modelName)[0]

        try:
            # Buscar o caminho completo
            lr = joblib.load(self.fullpathSelectedModel)
            y_pred = lr.predict(self.rows)

            # Criar um novo ficheiro e passar o resultado obtido apos a classificacao
            fileRefernce = open(f"{self.projectFolderPath}\\Results\\Classified_{modelNameSemExtensao}.txt", 'a+')


            for item in y_pred:
                fileRefernce.write(item + '\n')

            # Fechar o ficheiro
            fileRefernce.close()

            # Escrever no ficheiro de log
            self.log.logActions(f"Classification with model {modelNameSemExtensao} finished with success.")

            # Apresentar mensagem a dizer que a classificaçao correu bem
            messagebox.showinfo("Classification Done", "Classification finished with success!")

            # Fechar o ficheiro
            self.file.close()

            # Passar a variavel do self.ficheiroFoiAberto para 0
            self.ficheiroFoiAberto = 0

            # Retirar o self.rows e o self.target
            self.rows = []
            self.target = []


        except:
            # Apresentar mensagem caso dê erro
            messagebox.showerror("Error",
                                 f"Something went wrong when trying to classify with loaded model: {modelNameSemExtensao}")

            # Escrever no ficheiro de logs que deu erro
            self.log.logActions(f"Erro ao tentar classificar com o model carregado: {modelNameSemExtensao}")

            # Fechar o ficheiro
            self.file.close()

            # Passar a variavel do self.ficheiroFoiAberto para 0
            self.ficheiroFoiAberto = 0

            # Retirar o self.rows e o self.target
            self.rows = []
            self.target = []

        self.showLastCommand()


    def loadMetrics(self):
        metric = filedialog.askopenfilename(initialdir=f"{self.projectFolderPath}", title="Choose Model", filetypes=(
            ("TXT Files", "*.txt"),))
        metricName = os.path.basename(metric)
        metricNameSemExtensao = os.path.splitext(metricName)[0]

        # Caminho completo da metrica selecionada
        self.fullpathSelectedModel = metric

        # Fazer a divisao do resultado escolhido para conseguir ir buscar o ficheiro certo
        timestamp_data = metricNameSemExtensao.split("_")
        # Descobrir o dia
        day = timestamp_data[1]
        # Descobrir o mes
        month = timestamp_data[2]
        # Descobrir o ano
        year = timestamp_data[3]
        # Descobrir a hora
        hour = timestamp_data[4]
        # Descobrir o minuto
        minute = timestamp_data[5]
        # Separar os segundos do algoritmo
        second = timestamp_data[6]
        # Descobrir o algoritmo usado
        algoritmo = timestamp_data[7]
        # Descobrir o segundo
        # Obter a data correta e conforme o ficheiro guardado
        selectedResult = f"{day}-{month}-{year} {hour}:{minute}:{second} - {algoritmo}"

        self.lb_resultados.insert(END, selectedResult)


        # Creation of the space where we all tabs will be placed
        self.tab = Frame(self.notebook)
        self.notebook.add(self.tab, text=f"{selectedResult}")

        results = Text(self.tab)
        results.pack(expand=1, fill="both")

        file = open(metric, "r")

        for line in (file.readlines()):
            results.insert(INSERT, line.strip())
            results.insert(INSERT, '\n')


    def deleteMetrics(self):
        sel = self.lb_resultados.curselection()
        for name in sel:
            del self.dictResultados[f"{self.lb_resultados.index(name)}"]

        for index in sel[::-1]:
            self.lb_resultados.delete(index)

        lista_separadores = list(self.notebook.winfo_children())

        for index in sel[::-1]:
            for item in range(len(lista_separadores)):
                if index == item:
                    lista_separadores[index].destroy()
