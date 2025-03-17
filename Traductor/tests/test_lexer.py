import unittest
from lexer import Lexer

class TestLexer(unittest.TestCase):
    def test_valid_code(self):
        with open('samples/valid/correct.src') as f:
            code = f.read()
        
        lexer = Lexer()
        tokens = list(lexer.tokenize(code))
        
        # Verifica que el primer token sea 'PROGRAM'
        self.assertEqual(tokens[0].type, 'PROGRAM')
        
        # Verifica que exista token NUMBER
        self.assertTrue(any(t.type == 'NUMBER' for t in tokens))