import random
from enum import Enum
from finite_automaton import FiniteAutomaton


class GrammarTypology(str, Enum):
    RECURSIVELY_ENUMERABLE_GRAMMAR = "type_0"
    CONTEXT_SENSITIVE_GRAMMAR = "type_1"
    CONTEXT_FREE_GRAMMAR = "type_2"
    RIGHT_LINEAR_GRAMMAR = "type_3_right"
    LEFT_LINEAR_GRAMMAR = "type_3_left"


class Grammar:
    def __init__(self, VN, VT, P, S = "S"):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
    
    def generate_string(self):
        string = self.S
        while any(v in string for v in self.VN):
            for v in string:
                if v in self.VN:
                    string = string.replace(v, random.choice(self.P[v]), 1)
        return string
    
    def to_finite_automaton(self):
        q = self.VN
        sigma = self.VT
        q0 = self.S
        delta = {}
        for key in self.P.keys():
            delta[key] = [(item[0],) if len(item) == 1 else (item[0], item[1]) for item in self.P[key]]
        values = [item for sublist in self.P.values() for item in sublist]
        f = [item for item in values if len(set([key for key in self.P.keys()])-set(item)) == len(set([key for key in self.P.keys()]))]
        return FiniteAutomaton(q, sigma, delta, q0, f)
    
    def compute_type(self):
        is_type_0 = True
        is_type_1 = False
        is_type_2 = False
        is_type_3_right = False
        is_type_3_left = False

        
