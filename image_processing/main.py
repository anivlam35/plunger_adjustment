import sys, os, shutil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from filemanager import filesmanager, filemanager
from img_an_tm import cleaning_and_copying
from img_processing import calcs


# cleaning space
if 'results.txt' in os.listdir():
    os.remove('results.txt')

dir_c = os.getcwd()

class MainWindow(QMainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.initUI()
    
    # function for opening window with cropped image, thershold and plot with fitting 
    def load_image(self, file_name):
        self.w2 = AnotherWindow(file_name)
        self.w2.show()


    def initUI(self):

        imgs_for_processing = []
        tmplt_img = ''

	# calling filemanager from "filemanager.py" to select paths for template (first one) and source images (second one)
        def fm():
            global tmplt_img
            tmplt_img = filemanager()

        def fsm():
            global imgs_for_processing
            imgs_for_processing = filesmanager()


	# this is the function that does all the calculations
        def calculation():
            global imgs_for_processing
            global tmplt_img
            global dir_c
            try:
            	gr = int(layout_1v.itemAt(4).widget().text())
            except:
            	gr = 70
            os.chdir(dir_c)
            
            # cleaning workspace and copy selected images
            cleaning_and_copying(*imgs_for_processing)
            shutil.copy2(tmplt_img, os.getcwd() + '/template.png')
            
            # function from "img_processing.py" (description almost is there)
            calcs(gr, *imgs_for_processing)
            
            # filling box with results by text from "results.txt"
            res_qn.setText(open('results.txt').read())

            os.chdir(dir_c + '/cropped/')
            list_c = sorted(os.listdir())
	    
	    # making button with corresponding image as an icon 
            def build_btn(filenames, row, col):
                btn = QPushButton(self)
                btn.setMinimumHeight(150)
                btn.setStyleSheet("border-image : url(" + filenames[row * 8 + col] + ");")
                # btn.heightForWidth()
                pic_place.addWidget(btn, row, col)
                btn.clicked.connect(lambda: self.load_image(filenames[row * 8 + col]))

            bool_v = False
            for i in range(6):
                for j in range(8):
                    build_btn(list_c, i, j)
                    if list_c[i * 8 + j] == list_c[-1]:
                        bool_v = True
                        break
                if bool_v:
                    break



############################DESIGN GUI#####################################
        self.setWindowTitle('Image processing')
        self.resize(640, 480)
        # mlayout = QHBoxLayout()
        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout_main = QHBoxLayout()
        layout_1v = QGridLayout()
        layout_2t = QGridLayout()
        layout_2b = QGridLayout()
        layout_2 = QVBoxLayout()


        ########    LEFT PART   ########
        source_text = QLabel(self)
        source_text.setAlignment(Qt.AlignCenter)

        templ_text = QLabel(self)
        templ_text.setAlignment(Qt.AlignCenter)

        empty_label = QLabel(self)

        source_butt = QPushButton('Browse')
        source_text.setText("Source path")

        templ_butt = QPushButton('Browse')
        templ_text.setText("Template path")
        
        gr_edit = QLineEdit(self)

        calc_butt = QPushButton('Calculate')

        empty_label_2 = QLabel(self)

        layout_1v.addWidget(source_text, *(1, 0))
        layout_1v.addWidget(source_butt, *(2, 0))
        layout_1v.addWidget(templ_text, *(3, 0))
        layout_1v.addWidget(templ_butt, *(4, 0))
        layout_1v.addWidget(gr_edit, *(5, 0))
        layout_1v.addWidget(empty_label, *(6, 0))
        layout_1v.addWidget(calc_butt, *(7, 0))
        layout_1v.addWidget(empty_label_2, *(8, 0))

        layout_1v.setRowStretch(10, 7)

        ########    RIGHT PART   ########
        res_text = QLabel()
        res_text.setText('Results:')
        res_qn = QLabel()
        pic_place = QGridLayout()
        layout_2b.addWidget(res_text, *(1, 0))
        layout_2b.addWidget(res_qn, *(2, 0))

        layout_2t.addLayout(layout_2b, *(1,0), 1,1)
        layout_2t.addLayout(pic_place, *(2, 0), 11,11)


        source_butt.clicked.connect(fsm)
        templ_butt.clicked.connect(fm)
        calc_butt.clicked.connect(calculation)



        layout_main.addLayout(layout_1v, 1)
        layout_main.addLayout(layout_2t, 3)
        wid.setLayout(layout_main)


class AnotherWindow(QWidget):

    def __init__(self, image_for_showing):
        super().__init__()
        self.image_for_showing = image_for_showing
        self.my_window()
    
    # making window with cropped image, thershold and plot with fitting
    def my_window(self):
        global dir_c
        hbox = QHBoxLayout(self)

        pixmap2 = QPixmap(dir_c + '/plots/' + self.image_for_showing[:-12] + '_plot.png')
        lbl2 = QLabel(self)
        lbl2.setPixmap(pixmap2)

        pixmap = QPixmap(dir_c + '/cropped/' + self.image_for_showing[:-12] + '_cropped.png')
        pixmap1 = pixmap.scaled(pixmap.width(), pixmap2.height())
        lbl1 = QLabel(self)
        lbl1.setPixmap(pixmap1)
        lbl1.setMaximumHeight(600)

        pixmap_t = QPixmap(dir_c + '/thresholds/' + self.image_for_showing[:-12] + '_threshold.png')
        pixmap1_t = pixmap_t.scaled(pixmap_t.width(), pixmap2.height())
        lbl3 = QLabel(self)
        lbl3.setPixmap(pixmap1_t)
        lbl3.setMaximumHeight(600)

        hbox.addWidget(lbl1)
        hbox.addWidget(lbl3)
        hbox.addWidget(lbl2)
        self.setLayout(hbox)

        self.setWindowTitle(self.image_for_showing[:-12] + '_example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
