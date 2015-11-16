#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3 as lite
from bs4 import BeautifulSoup
from bs4 import NavigableString

class Verse():
    book = 0
    chapter = 0
    num = 0
    translation = 0
    text = ''
    alt_text = ''
    is_paragraph = False

def doSomething():
    f = open("OT/Bereshit/Bereshit02.htm","r")
    html_doc = f.read()

    soup = BeautifulSoup(html_doc)
    # print(soup.get_text())

    # print('all good inside parser')
    return soup.find_all(["p"])[0].get_text()

def parse(url):
    # record main or alternate text, according to flag
    def record_text(text):
        if use_alt: # WATCH OUT - this belongs to parse() parent method
            verse.alt_text += unicode(text)
        else:
            verse.text += unicode(text)

    # utility - clean extra spaces. add/expend at will
    def cleanup_verse():
        if verse.text:
            if verse.text[-1] in [')', '(']:
                verse.text = verse.text[:-1]
            verse.text = ' '.join(verse.text.split())
        if verse.alt_text:
            if verse.alt_text[-1] in [')', '(']:
                verse.alt_text = verse.alt_text[:-1]
            verse.alt_text = ' '.join(verse.alt_text.split())

    f = open(url,"r")
    html_doc = f.read()

    soup = BeautifulSoup(html_doc)
    # p = soup.p
    raw_text = soup.find(attrs={"name": "1"})

    verses = []
    verse = Verse()
    num = 0
    record = False
    record_next = False
    is_paragraph_next = True
    close_tag = ''
    inside_verse = False
    use_alt = False

    for e in raw_text.next_elements:
        if not isinstance(e, NavigableString):
            # print e.attrs
            if e.name == 'br':
                continue

            if e.name == 'b':
                #
                # TEST TEST TEST
                #

                # if 'class' in e.attrs:
                #     inside_verse = True
                #     num += 1
                #     verse.num = num
                #     if is_paragraph_next:
                #         verse.is_paragraph = True
                #         is_paragraph_next = False
                #     record_next = True
                # # else:
                # continue # this is for the html-1 b tag, ARGH

                #
                # ORIGINAL ORIGINAL ORIGINAL
                #
                if 'class' in e.attrs:
                    if inside_verse:    # should happen only on double-language (translated) parts
                        # print 'inside verse'
                        use_alt = True
                        record_next = True
                    else:
                        use_alt = False
                        inside_verse = True
                        num += 1
                        verse.num = num
                        if is_paragraph_next:
                            verse.is_paragraph = True
                            is_paragraph_next = False
                        record_next = True
                # else:
                continue # this is for the html-1 b tag, ARGH

            if e.name in ['big', 'small', 'span'] and record:
                # print "big!"
                record_text('<' + e.name + ' style="color:#CCC;">')
                # if use_alt:
                #     verse.alt_text += '<' + e.name + '>'
                # else:
                #     verse.text += '<' + e.name + '>'
                close_tag = '</' + e.name + '>'
                continue

            if e.get('name'):
                inside_verse = False
                record = False
                if e.get('name').isdigit():
                    cleanup_verse()

                    verses.append(verse)
                    verse = Verse()
                continue # this is for paragraph links

            if e.name in ['p', 'table']:
                is_inside_verse = False
                is_paragraph_next = True
                continue

            if e.name == 'a' and 'href' in e.attrs:
                record = False

            if e.name in ['table', 'colgroup', 'col', 'tr', 'td']:
                record = False

        if record_next:
            record_next = False
            record = True
            continue

        if record:
            record_text(unicode(e))
            if close_tag:
                record_text(close_tag)
                close_tag = ''

    cleanup_verse()         # don't forget to clean and append last verse
    verses.append(verse)

    return verses


# con = lite.connect('scriptures.db')
# with con:
#     cur = con.cursor()
#     # cur.execute("DROP TABLE Books")
#     # cur.execute("CREATE TABLE Books(Id INTEGER PRIMARY KEY, Name VARCHAR, Hebname VARCHAR)")
#     bla = doSomething()
#     cur.execute("INSERT INTO Books(Name, Hebname) VALUES('Bereshit', ?)", (bla,))
