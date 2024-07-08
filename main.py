from PyQt5 import QtWidgets
from ui import Ui_MainWindow
import sys
import JLink.ui_maneger as page


def ConnectUiWithEvent(ui):
    page.button_interface(ui)
  
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui  # Store the ui reference

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    MainWindow = MyMainWindow(ui)
    ui.setupUi(MainWindow)
    ConnectUiWithEvent(ui)
    page.ComboBoxInitialize(ui)
    page.page_color(ui)
    MainWindow.show()
    sys.exit(app.exec_())
