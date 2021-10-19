import joblib

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