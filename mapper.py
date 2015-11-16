#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
import parser

class Mapper():
    sections = {}

    for section_name in ["OT", "NT/Delitzsch", "NT/Modern"]:
        books = {}
        for root, dirs, files in os.walk(section_name + "/"):
            book_name = os.path.basename(root)
            if len(book_name) > 0:
                books[book_name] = {}
                for idx, file in enumerate(files):
                    if idx > 0:
                        books[book_name][idx] = os.path.join(root, file)
        sections[section_name] = books
def map():
    sections = {}

    for section_name in ["OT", "NT/Delitzsch", "NT/Modern"]:
        books = {}
        for root, dirs, files in os.walk(section_name + "/"):
            book_name = os.path.basename(root)
            if len(book_name) > 0:
                books[book_name] = {}
                for idx, file in enumerate(files):
                    if idx > 0:
                        books[book_name][idx] = os.path.join(root, file)
        sections[section_name] = books
    return sections

def main():
    mapper = Mapper()
    # verses = parser.parse(mapper.sections['OT']['Bereshit'][16])
    # for v in verses:
    #     print v.text
    for section_key, section_dict in mapper.sections.iteritems():
        for k, v in section_dict.iteritems():
            print len(v)

if __name__ == '__main__':
    main()

