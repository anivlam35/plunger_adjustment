from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

import sys, os

#This function creates window with cropped image, thresholded image and plot with fitting.
#It is connected to image-button (small picture of slit).

class AnotherWindow(QWidget):
     
    
    def __init__(self):
        super().__init__()

    def my_window(self, i):
        layout = QBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)

        hbox = QHBoxLayout(self)
        pixmap = QPixmap(os.getcwd() + '/cropped/' + str(i) + '_cropped.jpg')
        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        pixmap2 = QPixmap(os.getcwd() + '/cropped/' + str(i) + '_plot.png')
        lbl2 = QLabel(self)
        lbl2.setPixmap(pixmap2)
        hbox.addWidget(lbl1)
        hbox.addWidget(lbl2)
        self.setLayout(hbox)

        self.move(100, 200)
        self.setWindowTitle(str(i) + '_example')
        self.show()

app = QApplication(sys.argv)
app.setStyle('Fusion')
anw = AnotherWindow()
anw.show()
sys.exit(app.exec_())

my_window(1)
