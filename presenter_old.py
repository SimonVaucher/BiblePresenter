#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import parser, mapper, views

class Presenter(QWidget):
    def __init__(self, verses):
        super(Presenter, self).__init__()
        self.initUI(verses)
        self.verses = verses
        self.using_prefix_suffix = True

    def initUI(self, verses):
        verseModel = views.VerseModel(self, verses)

        self.verseView = QTableView()
        self.verseView.setModel(verseModel)
        self.verseView.verticalHeader().setVisible(False)
        selectionModel = self.verseView.selectionModel()
        selectionModel.selectionChanged.connect(self.selChanged)

        # with open("style.css", "r") as f:
        #     self.setStyleSheet(f.read())

        self.resize(550, 550)
        self.move(400, 200)
        self.setWindowTitle('presenter / parser test')

        self.txtEdit = QTextEdit()
        self.txtEdit.setLayoutDirection(Qt.RightToLeft)
        
        hbox = QHBoxLayout()
        # hbox.addStretch(0)
        hbox.addWidget(self.txtEdit)
        hbox.addWidget(self.verseView)
        self.setLayout(hbox)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def selChanged(self, new_selection, old_selection):
        numbers = []
        for model in self.verseView.selectionModel().selectedRows():
            numbers.append(model.row())
        if len(numbers) < 1:
            return

        numbers.sort()
        prev = None
        txt = ""
        for idx in numbers:
            if prev and (idx - prev) > 1:
                txt += u'<span style="font-size:1px; color:#fff;">א</span><span>...</span>'
            txt += u'<p style="color:#000;"><small class="bla">{} </small>{}</p>'.format(self.verses[idx].num, self.verses[idx].text)
            prev = idx
        if self.using_prefix_suffix:
            if numbers[0] > 0:
                txt = u'<p style="color:#CCC;"><small>{} </small>{}</p>'.format(self.verses[numbers[0] - 1].num, self.verses[numbers[0] - 1].text) + txt
            if numbers[-1] < (self.verses[-1].num - 1):
                txt += u'<p style="color:#CCC;"><small>{} </small>{}</p>'.format(self.verses[numbers[-1] + 1].num, self.verses[numbers[-1] + 1].text)

        txt = u'<span style="font-size: 1px; color:#fff;">א</span>' + txt
        self.txtEdit.setHtml(txt)

def main():
    # txt = parser.doSomething()
    # print txt[::-1]
    # url = "OT/Bereshit/Bereshit01.htm"
    url = "NT/Modern/Luke/Luke24.htm"
    # url = "OT/Tehillim/Tehillim49.htm"

    # CRAZY TABLE STUFF
    # url = "OT/Daniel/Daniel02.htm"

    verses = parser.parse(url)
    sections = mapper.Mapper()
    # txt = '<p>num of verses:{}</p>'.format(len(verses))
    # for v in verses:
    #     line = u'<small> {}</small> {}<em><strong> {}</strong></em>'.format(v.num, v.text, v.alt_text)
    #     if v.is_paragraph:
    #         line = "<p>" + line
    #     txt += line
    #     # print line
    #     # print v.num
    #     # print v.text
    #     # print v.alt_text

    # TODO:
    #
    # 1. Keep any parsed chapter in dict, like a primitive cache
    # 2. Parsing only whole chapter
    # 3. Verse selection is done later in presenter
    # 4. Above all - ease of navigation
    # 5. Any verse selection is recreating a long string, including inline css

    # txt = "<h1>test</h1>"
    # for v in verses:
    #     txt+=u'<p style="color:#AAA;"><small>{} </small>{}</p>'.format(v.num, v.text)
        # txt+=u'<p style="color:#AAA;"><small>{} </small>{}</p>'.format(v.num, v.alt_text)
    app = QApplication(sys.argv)
    
    presenter = Presenter(verses)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

