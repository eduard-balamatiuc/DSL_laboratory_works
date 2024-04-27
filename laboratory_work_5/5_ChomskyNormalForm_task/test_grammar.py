import unittest
from grammar import Grammar

class TestGrammar(unittest.TestCase):
    def test_start_symbol_check(self):
        VN = {"S", "A", "B", "C", "D", "E"}
        VT = {"a", "b"}
        P = {
            "S": ["aB", "AC"],
            "A": ["a", "ASC", "BC", "aD"],
            "B": ["b", "bS"],
            "C": ["", "BA"],
            "E": ["aB"],
            "D": ["abC"]
        }

        expected_result = {
            'VN': {'A', "S'", 'C', 'S', 'B', 'E', 'D'},
            'VT': {'b', 'a'},
            'P': {
                'S': ['aB', 'AC'],
                'A': ['a', 'ASC', 'BC', 'aD'],
                'B': ['b', 'bS'],
                'C': ['', 'BA'],
                'E': ['aB'],
                'D': ['abC'],
                "S'": ['S']
            },
            'S': "S'"
        }

        grammar = Grammar(VN, VT, P)
        grammar.start_symbol_check()
        self.assertEqual(grammar.to_dict(), expected_result)

    def test_remove_null_productions(self):
        VN = {'A', "S'", 'C', 'S', 'B', 'E', 'D'}
        VT = {"b", "a"}
        P = {
            'S': ['aB', 'AC'],
            'A': ['a', 'ASC', 'BC', 'aD'],
            'B': ['b', 'bS'],
            'C': ['', 'BA'],
            'E': ['aB'],
            'D': ['abC'],
            "S'": ['S']
        }
        S = "S'"

        expected_result = {
            'VN': {'D', 'E', 'A', 'B', 'S', 'C', "S'"},
            'VT': {'a', 'b'},
            'P': {
                'S': ['aB', 'AC', 'A'],
                'A': ['a', 'ASC', 'BC', 'aD', 'AS', 'B'],
                'B': ['b', 'bS'],
                'C': ['BA'],
                'E': ['aB'],
                'D': ['abC', 'ab'],
                "S'": ['S']
            },
            'S': "S'"
        }

        grammar = Grammar(VN, VT, P, S)
        grammar.remove_null_productions()
        self.assertEqual(grammar.to_dict(), expected_result)

    def test_remove_unit_productions(self):
        VN = {'D', 'E', 'A', 'B', 'S', 'C', "S'"}
        VT = {'a', 'b'}
        P = {
            'S': ['aB', 'AC', 'A'],
            'A': ['a', 'ASC', 'BC', 'aD', 'AS', 'B'],
            'B': ['b', 'bS'],
            'C': ['BA'],
            'E': ['aB'],
            'D': ['abC', 'ab'],
            "S'": ['S']
        }
        S = "S'"

        expected_result = {
            'VN': {'B', 'E', "S'", 'D', 'C', 'A', 'S'},
            'VT': {'b', 'a'},
            'P': {
                'S': ['aB', 'AC', 'a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS'],
                'A': ['a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS'],
                'B': ['b', 'bS'],
                'C': ['BA'],
                'E': ['aB'],
                'D': ['abC', 'ab'],
                "S'": ['aB', 'AC', 'a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS']
            },
            'S': "S'"
        }

        grammar = Grammar(VN, VT, P, S)
        grammar.remove_unit_productions()
        self.assertEqual(grammar.to_dict(), expected_result)

    def test_remove_two_or_more_symbols(self):
        VN = {'B', 'E', "S'", 'D', 'C', 'A', 'S'}
        VT = {'b', 'a'}
        P = {
            'S': ['aB', 'AC', 'a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS'],
            'A': ['a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS'],
            'B': ['b', 'bS'],
            'C': ['BA'],
            'E': ['aB'],
            'D': ['abC', 'ab'],
            "S'": ['aB', 'AC', 'a', 'ASC', 'BC', 'aD', 'AS', 'b', 'bS']
        }
        S = "S'"

        expected_result = {
            'VN': {'D*', 'A', 'S*', 'B', "S'", 'D', 'E', 'C', 'S'},
            'VT': {'b', 'a'},
            'P': {
                'S': ['aB', 'AC', 'a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
                'A': ['a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
                'B': ['b', 'bS'],
                'C': ['BA'],
                'E': ['aB'],
                'D': ['ab', 'aD*'],
                "S'": ['aB', 'AC', 'a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
                'S*': ['SC'],
                'D*': ['bC']
            },
            'S': "S'"
        }

        grammar = Grammar(VN, VT, P, S)
        grammar.remove_two_or_more_symbols()
        self.assertEqual(grammar.to_dict(), expected_result)

    def test_remove_terminal_and_variable_productions(self):
        VN = {'D*', 'A', 'S*', 'B', "S'", 'D', 'E', 'C', 'S'}
        VT = {'b', 'a'}
        P = {
            'S': ['aB', 'AC', 'a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
            'A': ['a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
            'B': ['b', 'bS'],
            'C': ['BA'],
            'E': ['aB'],
            'D': ['ab', 'aD*'],
            "S'": ['aB', 'AC', 'a', 'BC', 'aD', 'AS', 'b', 'bS', 'AS*'],
            'S*': ['SC'],
            'D*': ['bC']
        }
        S = "S'"

        expected_result = {
            'VN': {'D*', 'A', 'S*', 'b*', 'B', "S'", 'a*', 'D', 'E', 'C', 'S'},
            'VT': {'b', 'a'},
            'P': {
                'S': ['a*B', 'AC', 'a', 'BC', 'a*D', 'AS', 'b', 'b*S', 'AS*'],
                'A': ['a', 'BC', 'a*D', 'AS', 'b', 'b*S', 'AS*'],
                'B': ['b', 'b*S'],
                'C': ['BA'],
                'E': ['a*B'],
                'D': ['ab', 'a*D*'],
                "S'": ['a*B', 'AC', 'a', 'BC', 'a*D', 'AS', 'b', 'b*S', 'AS*'],
                'S*': ['SC'],
                'D*': ['b*C'],
                'a*': ['a'],
                'b*': ['b']
            },
            'S': "S'"
        }

        grammar = Grammar(VN, VT, P, S)
        grammar.remove_terminal_and_variable_productions()
        self.assertEqual(grammar.to_dict(), expected_result)

if __name__ == "__main__":
    unittest.main()
    