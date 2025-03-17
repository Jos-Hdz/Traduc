import unittest
from lexer import Lexer
from parser import Parser

class TestParser(unittest.TestCase):
    def test_invalid_syntax(self):
        with open('samples/invalid/syntax_errors.src') as f:
            code = f.read()
        
        tokens = list(Lexer().tokenize(code))
        
        with self.assertRaises(Exception):
            Parser(tokens).parse()