#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import parser, mapper, views, tuples

class OtherScreen(QWidget):
    def __init__(self):
        super(OtherScreen, self).__init__()
        widget = QDesktopWidget();
        width = widget.screenGeometry(2).width()
        height = widget.screenGeometry(2).height()

        self.resize(0.9*width, 0.9*height)
        self.move(widget.screenGeometry(2).topLeft())
        self.setWindowTitle('another screen')
        self.show()
        print "here!"

class Test(QWidget):
    def __init__(self):
        super(Test, self).__init__()
        widget = QDesktopWidget()
        # desk.screenGeometry(0) # main screenGeometry
        # desk.screenGeometry(1) # secondary screenGeometry
        # print desk.screenCount() # Duh
        self.show()
        # otherScreen = OtherScreen()

        widget = QDesktopWidget();
        width = widget.screenGeometry(0).width()
        height = widget.screenGeometry(0).height()


        otherScreen = OtherScreen()
        otherScreen.resize(0.9*width, 0.9*height)
        otherScreen.move(widget.screenGeometry(2).topLeft()) # important
        otherScreen.show()

        dialog = QDialog()
        dialog.show()
        # self.setWindowFlags(Qt.FramelesssWindowHint)
        # desk = QDesktopWidget()
        # # otherScreen.showFullScreen() # no reason to fiddle with it, it is a presenter
        # otherScreen.show() # no reason to fiddle with it, it is a presenter


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

def main():
    # TODO:
    #
    # 1. Show in external screen
    # 2. Buttons
    # 3. Minimal GUI 
    # 4. Keep global config for font size so it can be changed on the fly
    # 5. Keep some model of the selected verses outside of changed slot
    # 6. Set both viewport and preview to same "model" (generated text)
    # 7. Separate verse selection change and text redraw

    app = QApplication(sys.argv)    
    test = Test()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


# bla.txtView.setDocument(anotherBla.txtView.document())

# one QWidget >> presenter
# second QWidget >> "viewPort"

# inside the OTHER widget (full screen, secondary screen):
# >> self.setWindowFlags(Qt.FramelesssWindowHint)

# when showing viewport:
# >> self.viewport.move(desk.screenGeometry(1).topLeft()) # important
# >> self.viewport.showFullScreen() # no reason to fiddle with it, it is a presenter

