import random
from finite_automaton import FiniteAutomaton

class Grammar:
    def __init__(self, VN, VT, P, S):
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
        delta = self.P
        values = [item for sublist in self.P.values() for item in sublist]
        f = [item for item in values if len(set([key for key in self.P.keys()])-set(item)) == len(set([key for key in self.P.keys()]))]
        return FiniteAutomaton(q, sigma, delta, q0, f)
    
