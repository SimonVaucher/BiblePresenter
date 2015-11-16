#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

# DRYing up the code - all table models are a single column
class BaseColumnModel(QAbstractTableModel):
    def __init__(self, parent, data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data = data

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return 1


class TestamentModel(BaseColumnModel):
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return QVariant(self.data[index.row()][1])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return u"ברית"
        return QAbstractTableModel.headerData(self, section, orientation, role)


class BookModel(BaseColumnModel):
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return QVariant(self.data[index.row()][2])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return u"ספר"
        return QAbstractTableModel.headerData(self, section, orientation, role)


class ChapterModel(BaseColumnModel):
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return QVariant(self.data[index.row()][0])
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter
 
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return u"פרק"
        return QAbstractTableModel.headerData(self, section, orientation, role)


class VerseModel(BaseColumnModel):
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return QVariant(self.data[index.row()].num)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter | Qt.AlignVCenter

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return u"כל הפסוקים"
        return QAbstractTableModel.headerData(self, section, orientation, role)
