import unittest
from finite_automaton import FiniteAutomaton
from grammar import Grammar


"""
Variant 1
Q = {q0,q1,q2,q3},
∑ = {a,c,b},
F = {q2},
δ(q0,a) = q0,
δ(q0,a) = q1,
δ(q1,c) = q1,
δ(q1,b) = q2,
δ(q2,b) = q3,
δ(q3,a) = q1.
"""


class TestToRegularGrammar(unittest.TestCase):
    def test_to_regular_grammar_based_on_first_lab(self):
        q={"S", "Q", "P"}
        sigma={"e", "a", "b", "d", "f", "c"}
        delta={
            "S": [("a", "P"), ("b", "Q")],
            "P": [("b", "P"), ("c", "P"), ("d", "Q"), ("e",)],
            "Q": [("e", "Q"), ("f", "Q"), ("a",)]
        }
        q0="S"
        f=["e", "a"]
        test_finite_automaton = FiniteAutomaton(
            q=q,
            sigma=sigma,
            delta=delta,
            q0=q0,
            f=f,
        )

        expected_grammar = Grammar(
            VN={"S", "Q", "P"},
            VT={"e", "a", "b", "d", "f", "c"},
            P={
            "S": ["aP", "bQ"],
            "P": ["bP", "cP", "dQ", "e"],
            "Q": ["eQ", "fQ", "a"],
            },
        )
        self.assertEqual(test_finite_automaton.to_regular_grammar(), expected_grammar.to_dict())



if __name__=="__main__":
    unittest.main()