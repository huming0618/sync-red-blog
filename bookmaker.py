#coding=utf8
import os
import io

try:
    from BeautifulSoup import BeautifulSoup as BS
except ImportError:
    from bs4 import BeautifulSoup as BS

class bookmaker:
    
    def __init__(self, outputPath="output"):
        self.outputPath = outputPath
        self._soup = BS('', 'html')
        self._TOCItems = []
        self._Chapters = []

    def writeCoverPage(self):
        None

    def writeTOC(self, title='目录'):
        doc = self._soup
        TOCMark = doc.new_tag('a')
        TOCMark['name'] = 'TOC'

        TOCTitle_Center = doc.new_tag('center')
        TOCTitle_H1 = doc.new_tag('h1')
        TOCTitle_H1.string = title
        
        TOCTitle_Center.append(TOCTitle_H1)

        self._TOC = TOCTitle_Center
        #.append(doc.new_tag('h1')).append('目录')
        # doc.append(TOCMark)
        # doc.append(TOCTitle_Center)
    
    def writeTOCItem(self, name, title):
        doc = self._soup
        TOCItem = doc.new_tag('a')
        TOCItem['href'] = '#'+name
        
        TOCItemTitle = doc.new_tag('b')
        TOCItemTitle.string = title
        TOCItem.append(TOCItemTitle)

        self._TOCItems.append(TOCItem)


    def writeChapter(self, name, title, content):
        doc = self._soup
        chapterMark = doc.new_tag('a')
        chapterMark['name'] = name
        
        chapterTitle = doc.new_tag('h4')
        chapterTitle.string = title

        chapterContent = doc.new_tag('div')
        chapterContent.append(BS(content))

        self._Chapters.append((chapterMark, chapterTitle, chapterContent))

    def seal(self, name):
        doc = self._soup

        doc.append(self._TOC)

        for item in self._TOCItems:
            doc.append(item)
            doc.append(doc.new_tag('br'))

        doc.append(self._Chapters[0][2])

        with io.open(os.path.join(self.outputPath, 'book.html'), 'w', encoding='utf8') as temp:
            temp.write(doc.prettify())
