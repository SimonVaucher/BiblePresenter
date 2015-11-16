#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import parser, mapper, views, tuples

class Presenter(QWidget):
    def __init__(self, books):
        super(Presenter, self).__init__()
        self.books = books
        self.initUI()
        self.using_prefix_suffix = True
        self.cache = {}

    def initUI(self):
        self.testaments = [[u"OT", u"תנ״ך"], [u"NT/Modern", u"מודרני"], [u"NT/Delitzsch", u"דעליטש"]]
        self.testamentModel = views.TestamentModel(self, self.testaments)

        self.testamentView = QTableView()
        self.testamentView.verticalHeader().setVisible(False)
        self.testamentView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.testamentView.setModel(self.testamentModel)
        self.testamentView.selectionModel().selectionChanged.connect(self.selTestamentChanged)

        self.bookView = QTableView()
        self.bookView.verticalHeader().setVisible(False)
        self.bookView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.chapterView = QTableView()
        self.chapterView.verticalHeader().setVisible(False)
        self.chapterView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verseView = QTableView()
        self.verseView.verticalHeader().setVisible(False)

        self.txtView = QTextEdit()
        self.txtView.setReadOnly(True)
        self.txtView.setLayoutDirection(Qt.RightToLeft)

        widget = QDesktopWidget();
        width = widget.screenGeometry(0).width()
        height = widget.screenGeometry(0).height()

        self.resize(0.9*width, 0.9*height)
        self.move(0.05*width, 0.05*height)
        self.setWindowTitle('book tree')
      
        hbox = QHBoxLayout()
        hbox.addWidget(self.verseView)
        hbox.addWidget(self.chapterView)
        hbox.addWidget(self.bookView)
        hbox.addWidget(self.testamentView)

        rightBox = QHBoxLayout()
        rightBox.addLayout(hbox)

        leftBox = QHBoxLayout()
        leftBox.addWidget(self.txtView)

        layout = QHBoxLayout()
        layout.addLayout(leftBox, 3)
        layout.addLayout(rightBox, 2)

        self.setLayout(layout)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def selTestamentChanged(self, new_selection, old_selection):
        selected = self.testamentView.selectionModel().selectedRows()
        if len(selected) > 0:
            folder = self.testaments[selected[0].row()][0]
            paths = self.books.get(folder)

            self.booklist = []
            for tup in (tuples.ot if "OT" in folder else tuples.nt):
                temp = (tup[0], paths.get(tup[0]), tup[1]) # folder name, full path, hebrew book name
                self.booklist.append(temp)

            self.booksModel = views.BookModel(self, self.booklist)
            self.bookView.setSelectionMode(QAbstractItemView.SingleSelection)
            self.bookView.setModel(self.booksModel)
            self.bookView.selectionModel().selectionChanged.connect(self.selBookChanged)
            # self.bookView.resizeColumnsToContents()

            self.chapterView.setModel(None)
            self.verseView.setModel(None)
            self.txtView.setHtml("")


    def selBookChanged(self, new_selection, old_selection):
        selected = self.bookView.selectionModel().selectedRows()
        if len(selected) > 0:
            self.chapterlist = []
            for key, value in self.booklist[selected[0].row()][1].iteritems():
                temp = [key,value]
                self.chapterlist.append(temp)

            self.chapterModel = views.ChapterModel(self, self.chapterlist)
            self.chapterView.setModel(self.chapterModel)
            self.chapterView.selectionModel().selectionChanged.connect(self.selChapterChanged)

            self.verseView.setModel(None)
            self.txtView.setHtml("")


    def selChapterChanged(self, new_selection, old_selection):
        selected = self.chapterView.selectionModel().selectedRows()
        if len(selected) > 0:
            url = self.chapterlist[selected[0].row()][1]
            self.verses = self.cache.get(url)
            if not self.verses:
                self.verses = parser.parse(url)
                self.cache[url] = list(self.verses) # primitive but effective memory cache

            self.verseModel = views.VerseModel(self, self.verses)
            self.verseView.setModel(self.verseModel)
            self.verseView.selectionModel().selectionChanged.connect(self.selVerseChanged)
            # self.verseView.selectColumn(0) # optional - use to pre-select whole chapter

    def selVerseChanged(self, new_selection, old_selection):
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
            txt += u'<p style="color:#000; font-size:150%;"><small class="bla">{} </small>{}</p>'.format(self.verses[idx].num, self.verses[idx].text)
            prev = idx
        if self.using_prefix_suffix:
            if numbers[0] > 0:
                txt = u'<p style="color:#CCC;"><small>{} </small>{}</p>'.format(self.verses[numbers[0] - 1].num, self.verses[numbers[0] - 1].text) + txt
            if numbers[-1] < (self.verses[-1].num - 1):
                txt += u'<p style="color:#CCC;"><small>{} </small>{}</p>'.format(self.verses[numbers[-1] + 1].num, self.verses[numbers[-1] + 1].text)

        txt = u'<span style="font-size: 1px; color:#fff;">א</span>' + txt
        self.txtView.setHtml(txt)

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
    
    presenter = Presenter(mapper.map())
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
