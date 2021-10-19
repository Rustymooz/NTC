import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.datasets import load_iris
import pandas
import numpy
import File
import LogFile
import ProjectLogFile
import sklearn.externals

# IMPORT do messagebox
from tkinter import messagebox

# IMPORT para apresentar a data
from datetime import datetime

# IMPORT para apresentar graficos
# É preciso instalar um package
import matplotlib.pyplot as plt


class NB:
    def __init__(self):
        pass

    def NB(self, projectFolderPath, X_train, X_test, y_train, y_test):
        #X_train, X_test, y_train, y_test = train_test_split(rows, target, test_size=test_size)
        nb = GaussianNB()

        # TRY
        # Fazer o fit
        try:
            nb.fit(X_train, y_train)
        # Abrir uma mensagem de erro a dizer que nao foi possivel fazer o fit
        except:
            messagebox.showerror("Error", "Verify number of classes of target column")
            return


        y_pred = nb.predict(X_test)

        # Get current timestamp
        now = datetime.now()
        current_timestamp = now.strftime("%d_%m_%Y_%H_%M_%S")
        # Create a file with model
        joblib.dump(nb, f'{projectFolderPath}\\Models\\NaiveBayesmodel_{current_timestamp}.pkl')

        # Todas as metricas necessarias
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

        # Construir o grafico da metrica ROC Curve
        metrics.plot_roc_curve(nb, X_test, y_test)
        # Guardar o grafico
        plt.savefig(f'{projectFolderPath}\\Plots\\NBmodel_{current_timestamp}_ROCCurve.png')

        # Construir o grafico da CONFUSION MATRIX
        metrics.plot_confusion_matrix(nb, X_test, y_test)
        # Guardar o grafico
        plt.savefig(f'{projectFolderPath}\\Plots\\NBmodel_{current_timestamp}_ConfusionMatrix.png')

        # Construir o grafico da metrica PRECISION RECALL
        metrics.plot_precision_recall_curve(nb, X_test, y_test)
        # Guardar o grafico
        plt.savefig(f'{projectFolderPath}\\Plots\\NBmodel_{current_timestamp}_PrecisionRecallCurve.png')

        return dictionary, current_timestamp



        # write in the log file
        #self.log.logActions(f"Gaussian Naive Bayes aplied")