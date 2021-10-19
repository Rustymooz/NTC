#import category_encoders
from tkinter import messagebox
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

import File
import statistics
import File

class Table:

    def __init__(self, dataFile):
        self.dataFile = dataFile
        # self.statFile = statFile

    def setValue(self, lineIndex, columnIndex, value):
        self.dataFile.setValue(lineIndex, columnIndex, value)

    def getValue(self, lineIndex, columnIndex):
        return self.dataFile.getValue(lineIndex, columnIndex)

    def getColumnNames(self):
        colunas = self.dataFile.getLine(0)
        return colunas

    def getLine(self, lineIndex):
        return self.dataFile.getLine(lineIndex)

    def deleteColumn(self, columnIndex):
        self.dataFile.setColumn(columnIndex, None)

    def deleteLine(self, lineIndex):
        self.dataFile.setLine(lineIndex, None)

    def getColumn(self, columnIndex):
        return self.dataFile.getColumn(columnIndex)

    def closeFiles(self):
        self.dataFile.closeFile()
        # self.statFile.closeFile()

    def calculateMean(self, columnIndex):
        # array to put values to calculate mean
        values = []
        # get the specified column
        column = self.dataFile.getColumn(columnIndex)
        # loop all the lines in the column
        for elem in range(1, len(column)):
            if column[elem] == '*':
                pass
            else:
                elem = float(column[elem])
                # verify if is not string
                if type(elem) != str:
                    values.append(elem)
        # return mean
        return statistics.mean(values)

    def calculateMedian(self, columnIndex):
        # Array to put elements to calculate median
        medianArray = []
        # get the specified column
        column = self.dataFile.getColumn(columnIndex)
        # Loop all the lines in the column
        for elem in range(1, len(column)):
            if column[elem] == '*':
               pass
            else:
                elem = float(column[elem])
                # Verify null value
                if type(elem) != str:
                    medianArray.append(elem)
        # Return median
        return statistics.median(medianArray)

    def calculateMax(self, columnIndex):
        values = []
        column = self.dataFile.getColumn(columnIndex)
        # Loop all the lines in the column
        for elem in range(1, len(column)):
            try:
                elem = float(column[elem])
            except:
                pass

            # Verify null value
            if type(elem) != str:
                values.append(elem)
        # Return median
        return max(values)

    def calculateMin(self, columnIndex):
        values = []
        column = self.dataFile.getColumn(columnIndex)
        # Loop all the lines in the column
        for elem in range(1, len(column)):
            try:
                elem = float(column[elem])
            except:
                pass
            # Verify null value
            if type(elem) != str:
                values.append(elem)
        # Return median
        return min(values)

    # calcular a quantidade de linha da tabela
    def quantityOfValues(self):
        return self.dataFile.fileNumLines

    # calcular o numero de linhas com valores a null
    def numOfLinesWithNullValues(self, columnIndex):
        linesWithNullValues = 0
        for line in range(0, self.dataFile.fileNumLines):
            value = self.dataFile.getValue(line, columnIndex)
            if value == "*":
                linesWithNullValues += 1
        return linesWithNullValues

    def replaceNullValues(self, columnIndex, valueToReplace):
        for elem in range(1, self.dataFile.fileNumLines):
            value = self.getValue(elem, columnIndex)
            if value == '*':
                self.setValue(elem, columnIndex, valueToReplace)

    def replaceCertain(self, columnIndex, valueToReplace, targetValue):
        for elem in range(1, self.dataFile.fileNumLines):
            value = self.getValue(elem, columnIndex)
            if value == targetValue:
                self.setValue(elem, columnIndex, valueToReplace)

    def checkIfNotNumeric(self, columnIndex):
        column = self.getColumn(columnIndex)
        for elem in column:
            if type(elem) != str:
                return False
        return True

    def getColumnTypes(self, columnIndex):
        if not self.checkIfNotNumeric(columnIndex):
            print("Column has numeric values")
        types = dict()
        oldColumn = self.getColumn(columnIndex)
        for i in range(1, len(oldColumn)):
            elem = oldColumn[i]
            if elem not in types:
                types.update({elem: 1})
            else:
                count = types.get(elem)
                count += 1
                types.update({elem: count})
        lista = list(types)
        newColumn = []
        newColumn.append(oldColumn[0])
        for i in range(1, len(oldColumn)):
            elem = oldColumn[i]
            newColumn.append(lista.index(elem))
        self.dataFile.setColumn(columnIndex, newColumn)


    def ordinalEncoding(self, filepath):
        path = Path(filepath)
        projectFolderPath = path.parent.absolute()

        df = pd.read_csv(filepath)
        encoder = OrdinalEncoder()
        df[df.select_dtypes(include=['object']).columns] = encoder.fit_transform(df.select_dtypes(include=['object']))
        df.head()
        df.to_csv(f"{projectFolderPath}\\teste2.csv", index=False)
        datafile2 = File.File()
        datafile2.openDataFile(f"{projectFolderPath}\\teste2.csv")
        for col in range(0, self.dataFile.fileNumColumns):
            for line in range(1, self.dataFile.fileNumLines):
                value = datafile2.getValue(line, col)
                self.dataFile.setValue(line, col, value)
        datafile2.closeFile()
        self.dataFile.updateFile()


    def oneHotEncoding(self, filepath):
        path = Path(filepath)
        projectFolderPath = path.parent.absolute()

        df = pd.read_csv(filepath)
        encoder = OneHotEncoder()
        df[df.select_dtypes(include=['object']).columns] = encoder.fit_transform(df.select_dtypes(include=['object']))
        df.head()
        df.to_csv(f"{projectFolderPath}\\teste2.csv", index=False)
        datafile2 = File.File()
        datafile2.openDataFile(f"{projectFolderPath}\\teste2.csv")
        for col in range(0, self.dataFile.fileNumColumns):
            for line in range(1, self.dataFile.fileNumLines):
                value = datafile2.getValue(line, col)
                self.dataFile.setValue(line, col, value)
        datafile2.closeFile()
        self.dataFile.updateFile()

    def z_score(self, filepath, targetColumn):
        path = Path(filepath)
        projectFolderPath = path.parent.absolute()

        df = pd.read_csv(filepath)

        if not targetColumn:
            messagebox.showerror("Target column not found", "Choose target column before apply z-score")
        else:
            for column in df.select_dtypes(exclude=['object']).columns:
                if column != targetColumn:
                    if df[column].std() == 0:
                        pass
                    else:
                        df[column] = (df[column] - df[column].mean()) / df[column].std()

            df.to_csv(f"{projectFolderPath}\\teste2.csv", index=False)
            datafile2 = File.File()
            datafile2.openDataFile(f"{projectFolderPath}\\teste2.csv")
            for col in range(0, self.dataFile.fileNumColumns):
                for line in range(1, self.dataFile.fileNumLines):
                    value = datafile2.getValue(line, col)
                    self.dataFile.setValue(line, col, value)
            datafile2.closeFile()
            self.dataFile.updateFile()




