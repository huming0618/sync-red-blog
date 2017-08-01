#coding=utf8
import os
import io
from jinja2 import Environment, FileSystemLoader, select_autoescape



MEDIA_TYPE_TEXT = 'text/x-oeb1-document';
MEDIA_TYPE_XML = 'application/x-dtbncx+xml'

class book(object):
    def __init__(self):
        self.book_coverimage = ''
        self.book_title = ''
        self.book_author = ''
        self.book_publisher = ''
        self.toc_title = ''
        self.toc_image = ''
        self.toc = []
        self.navpoint = []
    
    def pack(self):
        return self.__dict__

    

class bookmaker:
    
    def __init__(self, templatePath="template", outputPath="output"):
        self.output_path = outputPath
        self.template_path = templatePath
        self.book = book()
        self.tplenv = Environment(
            loader=FileSystemLoader(searchpath=self.template_path)
        )

    def writeTitle(self, title='the book'):
        self.book.book_title = title

    def writeCoverImage(self, image='images/cover.jpg'):
        self.book.book_coverimage = image

    def writeTOCTitle(self, title='目录', image=''):
        self.book.toc_title = title
        self.book.toc_image = image
    
    def writeTOCItem(self, item_title, item_name):
        item_href = '#' + item_name
        self.book.toc.append(dict(href=item_href, title=item_title))

    def writeTOCFileLinkItem(self, item_title, item_file, item_name):
        item_href = item_file
        if item_name:
            item_href = item_href + '#' + item_name
        self.book.toc.append(dict(href=item_href, title=item_title))

    def writeNavPointItem(self, item_title, item_name, item_order):
        item_href = '#' + item_name
        self.book.navpoint.append(dict(href=item_href, title=item_title, id=item_name, order=item_order))

    def writeNavPointFileLinkItem(self, item_title, item_file, item_name, item_order, name_for_hash=False):
        item_href = item_file
        if name_for_hash:
            item_href = item_href + '#' + item_name
        self.book.navpoint.append(dict(href=item_href, title=item_title, id=item_name, order=item_order))

    def writeChapter(self, name, chapter_title, chapter_content, chapter_subtitle='', chapter_headimage=''):
        output_file = os.path.join(self.output_path, name + '.html')
        tpl = self.tplenv.get_template('chapter.html')
        text = tpl.render(title=chapter_title, content=chapter_content, subtitle=chapter_subtitle, header_image=chapter_headimage)

        with io.open(output_file, 'w') as temp:
            temp.write(text)

    def make_opf(self):
        None

    def make_toc(self):
        output_file = os.path.join(self.output_path, 'toc.html')
        tpl = self.tplenv.get_template('toc.html')
        
        text = tpl.render(self.book.pack())

        
        with io.open(output_file, 'w', encoding='utf8') as temp:
            temp.write(text)
    
    def make_ncx(self):
        output_file = os.path.join(self.output_path, 'toc.ncx')
        tpl = self.tplenv.get_template('ncx.xml')
        text = tpl.render(self.book.pack())

        with io.open(output_file, 'w', encoding='utf8') as temp:
            temp.write(text)

    def seal(self):
        #make_opf()
        self.make_toc()
        self.make_ncx()

        # output_file = os.path.join(self.output_path, name + '.html')
        # tpl = env.get_template('chapter.html')
        # text = tpl.render(title=chapter_title, content=chapter_content)

        # with io.open(output_file, 'w') as temp:
        #     temp.write(text)
