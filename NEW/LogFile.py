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

class LogFile:

    def __init__(self, projectPath):
        # path to save the file with the project configurations
        self.filePath = f"{projectPath}\log.txt"
        # reference to the opened file
        self.fileReference = None
        # number of lines in the file
        self.numOfLines = 0

    def logActions(self, message):
        logging.basicConfig(filename=self.filePath, level=logging.INFO, format='%(asctime)s - %(message)s')
        logging.info(message)
