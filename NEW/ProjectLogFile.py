import csv
import logging
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from shutil import copyfile
import datetime
from tkinter.ttk import Notebook
import numpy
from sklearn import preprocessing as pp
from sklearn import model_selection as ms
#import keras_preprocessing
#import category_encoders as ce
import File
import Table

class ProjectLogFile:
    def __init__(self, filePath):
        # path to save the file with the project configurations
        self.filePath = filePath
        # reference to the opened file
        self.fileReference = open(self.filePath, 'a+')

    def writeLine(self, line):
        self.fileReference.write(line + '\n')

    def readLine(self):
        self.fileReference.readline()

    def closeFile(self):
        self.fileReference.close()