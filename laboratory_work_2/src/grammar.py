import random
from enum import Enum
from finite_automaton import FiniteAutomaton


class GrammarTypology(str, Enum):
    """Enum class for the different types of grammars. 
    The values are the same as the ones used in the Chomsky hierarchy based on the LFPC Guide.
    """
    RECURSIVELY_ENUMERABLE_GRAMMAR = "type_0"
    CONTEXT_SENSITIVE_GRAMMAR = "type_1"
    CONTEXT_FREE_GRAMMAR = "type_2"
    RIGHT_LINEAR_GRAMMAR = "type_3_right"
    LEFT_LINEAR_GRAMMAR = "type_3_left"


class Grammar:
    """Class representing a generalised grammar."""
    def __init__(self, VN, VT, P, S="S"):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.type = self.compute_type()  # Compute the grammar type during initialization

    def __str__(self):
        """Printable representation of the grammar."""
        return f"{self.type} grammar: VN={self.VN}, VT={self.VT}, P={self.P}, S={self.S}"

    def generate_string(self):
        """Generates a random string from the grammar."""
        string = self.S
        while any(v in string for v in self.VN):
            for v in string:
                if v in self.VN:
                    string = string.replace(v, random.choice(self.P[v]), 1)
        return string

    def to_finite_automaton(self):
        """Function to convert a grammar to a finite automaton."""
        q = self.VN
        sigma = self.VT
        q0 = self.S
        delta = {}
        for key in self.P.keys():
            delta[key] = [(item[0],) if len(item) == 1 else (item[0], item[1]) for item in self.P[key]]
        values = [item for sublist in self.P.values() for item in sublist]
        f = [item for item in values if len(set(self.P.keys())-set(item)) == len(set(self.P.keys()))]
        return FiniteAutomaton(q, sigma, delta, q0, f)

    def compute_type(self):
        """Function to compute the type of the grammar based on the Chomsky hierarchy."""
        is_type_2 = True
        is_type_3_right = True
        is_type_3_left = True

        for left_keys, right_values in self.P.items():
            if len(left_keys) > 1:
                return GrammarTypology.RECURSIVELY_ENUMERABLE_GRAMMAR.value

            for right_value in right_values:
                # Context-sensitive check (any rule where the length of the right_value is less than the left_keys)
                if len(right_value) < len(left_keys):
                    return GrammarTypology.RECURSIVELY_ENUMERABLE_GRAMMAR.value

                # Context-free check
                if any(char in self.VN for char in right_value[1:]):
                    is_type_2 = False

                # Right-linear check
                if not (len(right_value) == 1 and right_value[-1] in self.VT) and not (right_value[-1] in self.VN and all(char in self.VT for char in right_value[:-1])):
                    is_type_3_right = False
                
                # Left-linear check
                if not (len(right_value) == 1 and right_value[0] in self.VT) and not (right_value[0] in self.VN and all(char in self.VT for char in right_value[1:])):
                    is_type_3_left = False

        if is_type_2:
            return GrammarTypology.CONTEXT_FREE_GRAMMAR.value
        if is_type_3_right:
            return GrammarTypology.RIGHT_LINEAR_GRAMMAR.value
        if is_type_3_left:
            return GrammarTypology.LEFT_LINEAR_GRAMMAR.value

        return GrammarTypology.CONTEXT_SENSITIVE_GRAMMAR.value
