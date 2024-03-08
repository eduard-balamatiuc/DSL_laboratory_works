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

    def test_to_regular_grammar_based_on_second_lab(self):
        q = {"0", "1", "2", "3"}
        sigma = {"a", "c", "b"}
        delta = {
            "0": [("a", "0"), ("a", "1")],
            "1": [("c", "1"), ("b", "2")],
            "2": [("b", "3")],
            "3": [("a", "1")]
        }
        q0 = "0"
        f = ["2"]
        test_finite_automaton = FiniteAutomaton(
            q=q,
            sigma=sigma,
            delta=delta,
            q0=q0,
            f=f,
        )
        expected_grammar = Grammar(
            VN={"0", "1", "2", "3"},
            VT={"a", "c", "b"},
            P={
                "0": ["a0", "a1"],
                "1": ["c1", "b2"],
                "2": ["b3"],
                "3": ["a1"]
            },
            S="0"
        )
        self.assertEqual(test_finite_automaton.to_regular_grammar(), expected_grammar.to_dict())


class TestIsDeterministic(unittest.TestCase):
    def test_is_deterministic_based_on_first_lab(self):
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
        self.assertTrue(test_finite_automaton.is_deterministic())

    def test_is_deterministic_based_on_second_lab(self):
        q = {"0", "1", "2", "3"}
        sigma = {"a", "c", "b"}
        delta = {
            "0": [("a", "0"), ("a", "1")],
            "1": [("c", "1"), ("b", "2")],
            "2": [("b", "3")],
            "3": [("a", "1")]
        }
        q0 = "0"
        f = ["2"]
        test_finite_automaton = FiniteAutomaton(
            q=q,
            sigma=sigma,
            delta=delta,
            q0=q0,
            f=f,
        )
        self.assertFalse(test_finite_automaton.is_deterministic())


if __name__=="__main__":
    unittest.main()