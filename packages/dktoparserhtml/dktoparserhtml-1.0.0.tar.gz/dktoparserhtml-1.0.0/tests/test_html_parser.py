# -*- coding: utf-8 -*-
import unittest  # python -m unittest discover
import sys
sys.path.insert(0, '../')
from module_html_parser import ParserHTML

class TestParserHTML(unittest.TestCase):
    def setUp(self):
        # Code execute avant chaque test

        self.content_utf8 = """
A: . à ä â - . À Ä Â
E: é è ë ê - É È Ë Ê
I: . . ï î - . . Ï Î
<i>Un texte en italique</i>
<b><u>Un texte gras et souligné</u></b>
"""
        self.content_html="""
A: . &agrave; &auml; &acirc; &minus; . &Agrave; &Auml; &Acirc;
E: &eacute; &egrave; &euml; &ecirc; &minus; &Eacute; &Egrave; &Euml; &Ecirc;
I: . . &iuml; &icirc; &minus; . . &Iuml; &Icirc;
<i>Un texte en italique</i>
<b><u>Un texte gras et soulign&eacute;</u></b>
"""

        self.content_md="""
A: . à ä â - . À Ä Â
E: é è ë ê - É È Ë Ê
I: . . ï î - . . Ï Î
*Un texte en italique*
**__Un texte gras et souligné__**
"""

        self.my_class_instance = ParserHTML()
    #endDef


    def test_utf8_to_html(self):
        self.my_class_instance.data = self.content_utf8
        result = self.my_class_instance.utf8_to_html()
        self.assertEqual(result, self.content_html)
    #endDef


    def test_html_to_utf8(self):
        self.my_class_instance.data = self.content_html
        result = self.my_class_instance.html_to_utf8()
        self.assertEqual(result, self.content_utf8)
    #endDef


    def test_html_to_markdown(self):
        self.my_class_instance.data = self.content_html
        result = self.my_class_instance.html_to_markdown()
        self.assertEqual(result, self.content_md)
    #endDef


    def tearDown(self):
        # Code exécuté après chaque test
        del self.my_class_instance
    #endDef
#endClass
