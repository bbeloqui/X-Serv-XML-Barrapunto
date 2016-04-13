#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.title = " "
        self.response = " "

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.inContent = False
                line_title = '\n<h1>Title:</h1>'+ '<h2><a href="'
                line_title += self.theContent
                line_title += '">'
                line_title += self.title + '</a></h2>'
                self.response += line_title
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog
if __name__ == "__main__":
    if len(sys.argv)<2:
        print "Usage: python xml-parser-barrapunto.py <document>"
        print
        print " <document>: file name of the document to parse"
        sys.exit(1)

# Load parser and driver

    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)

# Ready, set, go!

    xmlFile = open(sys.argv[1],"r")
    theParser.parse(xmlFile)

    htmlResponse = open("archivo.html", "w")
    htmlResponse.write(theHandler.response.encode("utf-8"))
