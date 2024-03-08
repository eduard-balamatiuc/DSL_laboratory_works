import unittest
from grammar import Grammar, GrammarTypology


class TestGrammar(unittest.TestCase):
    def test_compute_type(self):
        # Test for RECURSIVELY_ENUMERABLE_GRAMMAR grammar
        grammar = Grammar(
            VN={"S", "B"},
            VT={"x", "y"},
            P={"Syx": ["xy"], "B": ["S"]},
        )
        self.assertEqual(grammar.type, GrammarTypology.RECURSIVELY_ENUMERABLE_GRAMMAR.value)

        # Test for CONTEXT_SENSITIVE_GRAMMAR grammar
        grammar = Grammar(
            VN={"S", "Q"},
            VT={"0", "1", "2"},
            P={"S": ["QR"], "Q": ["012"], "R": ["1"]},
        )
        self.assertEqual(grammar.type, GrammarTypology.CONTEXT_SENSITIVE_GRAMMAR.value)

        # Test for CONTEXT_FREE_GRAMMAR grammar
        grammar = Grammar(
            VN={"S", "Q", "R"},
            VT={"x", "y", "z"},
            P={"S": ["Qz"], "Q": ["yR"], "R": ["x"]},
        )
        self.assertEqual(grammar.type, GrammarTypology.CONTEXT_FREE_GRAMMAR.value)

        # Test for RIGHT_LINEAR_GRAMMAR grammar
        grammar = Grammar(
            VN={"S", "Q", "R", "T"},
            VT={"0", "1", "2"},
            P={"S": ["0Q", "1R"], "Q": ["1S", "2T", "0"], "R": ["2Q"], "T": ["0", "2R"]},
        )
        self.assertEqual(grammar.type, GrammarTypology.RIGHT_LINEAR_GRAMMAR.value)

        # Test for LEFT_LINEAR_GRAMMAR grammar
        grammar = Grammar(
            VN={"S", "Q", "R", "T"},
            VT={"a", "b", "c"},
            P={"S": ["Qa", "Ra"], "Q": ["Sb", "Tc", "c"], "R": ["Qb"], "T": ["b", "Rc"]},
        )
        self.assertEqual(grammar.type, GrammarTypology.LEFT_LINEAR_GRAMMAR.value)


if __name__ == "__main__":
    unittest.main()