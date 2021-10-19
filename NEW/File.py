import os


class File:

    def __init__(self):
        self.filePath = ""
        # reference to the open file
        self.fileReference = None
        # number of lines and columns of the file
        self.fileNumLines = 0
        self.fileNumColumns = 0
        # array that stores the lines in the file
        self.lines = []

    def initDataFile(self, dataFilePath, newDataFilePath):
        # open the original data file for reading
        dataFile = open(dataFilePath, 'r')
        # set the path of the new data file
        self.filePath = newDataFilePath
        # create the new data file and open it for reading and writing
        self.fileReference = open(self.filePath, 'w')

        self.lines = dataFile.readlines()
        self.fileNumLines = len(self.lines)
        dataFile.close()

        newLines = []
        for i in range(0, self.fileNumLines):
            line = self.lines.pop(0)
            line = self.fixEmptyCommas(line)
            newLines.append(self.stringToComponents(line))
        self.lines = newLines


        self.fileNumColumns = len(self.lines[0])

    def openDataFile(self, filePath):
        # get the data file path
        self.filePath = filePath
        # open the data file
        self.fileReference = open(self.filePath, 'r')

        self.lines = self.fileReference.readlines()
        self.fileNumLines = len(self.lines)

        newLines = []
        for i in range(0, self.fileNumLines):
            line = self.lines.pop(0)
            line = self.fixEmptyCommas(line)
            newLines.append(self.stringToComponents(line))
        self.lines = newLines


        self.fileNumColumns = len(self.lines[0])

    def close(self):
        # close the file
        self.fileReference.close()

    def closeFile(self):
        # force update the file
        self.updateFile()
        # close the file
        self.fileReference.close()

    def getValue(self, lineIndex, columnIndex):
        return self.lines[lineIndex][columnIndex]

    def setValue(self, lineIndex, columnIndex, newValue):
        self.lines[lineIndex][columnIndex] = newValue

    def getLine(self, lineIndex):
        line = []
        for i in range(0, self.fileNumColumns):
            line.append(self.lines[lineIndex][i])
        return line

    def setLine(self, lineIndex, newLine):
        if newLine is None:
            self.lines.pop(lineIndex)
            self.fileNumLines -= 1
            return
        for i in range(0, self.fileNumColumns):
            self.lines[lineIndex][i] = newLine[i]

    def getColumn(self, columnIndex):
        column = []
        for i in range(0, self.fileNumLines):
            column.append(self.lines[i][columnIndex])
        return column

    def setColumn(self, columnIndex, newColumn):
        if newColumn is None:
            for i in range(0, self.fileNumLines):
                self.lines[i].pop(columnIndex)
            self.fileNumColumns -= 1
            return
        for i in range(0, self.fileNumLines):
            self.lines[i][columnIndex] = newColumn[i]

    # --------------------------------------------------------------------------

    def fixEmptyCommas(self, string):
        # split the string char by char
        components = []
        components[0:] = string
        # first base case (comma at the beginning of the components array)
        if components[0] == ',':
            components.insert(0, '*')
        # last base case (comma at the end of the components array)
        if components[-1] == ',':
            components.append('*')
        # all other cases
        # iterate through the components array
        index = 0
        while index < len(components) - 1:
            # check for two consecutive commas
            if components[index] == ',' and components[index + 1] == ',':
                # insert spacer
                components.insert(index + 1, '*')
            index += 1
        # return components as a string
        return "".join(components)

    def stringToComponents(self, string):
        if string[-1] == '\n':
            string = string[:-1]
        chars = list(string)
        isString = False
        component = ""
        components = []
        for c in chars:
            isComma = (c == ',')
            isString = (not isString) if (c == '\"') else isString
            if isComma and isString:
                component += c
            elif isComma:
                components.append(component)
                component = ""
            else:
                component += c
        components.append(component)
        for i in range(0, len(components)):
            if type(components[i]) == str and components[i].isnumeric():
                components[i] = float(components[i])
        return components

    def componentsToString(self, components):
        for i in range(0, len(components)):
            if type(components[i]) != str:
                components[i] = str(components[i])
        string = ','.join(components) + '\n'
        return string

    def updateFile(self):
        self.fileReference.close()
        self.fileReference = open(self.filePath, 'w')

        newLines = []
        for i in range(0, self.fileNumLines):
            line = self.lines[i]
            newLines.append(self.componentsToString(line))

        self.fileReference.writelines(newLines)
        self.fileReference.close()