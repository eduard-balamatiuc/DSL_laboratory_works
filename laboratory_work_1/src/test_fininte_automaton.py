import unittest
from finite_automaton import FiniteAutomaton
from grammar import Grammar

class TestFiniteAutomaton(unittest.TestCase):
    def test_string_belong_to_language(self):
        VN = {'S', 'P', 'Q'}
        VT = {'a', 'b', 'c', 'd', 'e', 'f'}
        P = {
            'S': ['aP', 'bQ'],
            'P': ['bP', 'cP', 'dQ', 'e'],
            'Q': ['eQ', 'fQ', 'a']
        }
        S = 'S'
        grammar = Grammar(VN, VT, P, S)
        finiteAutomaton = grammar.to_finite_automaton()

        self.assertFalse(finiteAutomaton.string_belong_to_language('ab'))
        self.assertFalse(finiteAutomaton.string_belong_to_language('bce'))
        self.assertTrue(finiteAutomaton.string_belong_to_language('bdfa'))
        self.assertTrue(finiteAutomaton.string_belong_to_language('ae'))
        self.assertTrue(finiteAutomaton.string_belong_to_language('adea'))
        self.assertTrue(finiteAutomaton.string_belong_to_language('abbbbbbbbbbbbbbda'))

if __name__ == '__main__':
    unittest.main()