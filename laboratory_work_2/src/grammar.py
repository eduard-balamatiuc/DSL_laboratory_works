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
    def __init__(self, VN, VT, P, S="S") -> None:
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
        self.type = self.compute_type()  # Compute the grammar type during initialization

    def __str__(self) -> str:
        """Printable representation of the grammar."""
        return f"{self.type} grammar: VN={self.VN}, VT={self.VT}, P={self.P}, S={self.S}"

    def generate_string(self) -> str:
        """Generates a random string from the grammar."""
        string = self.S
        while any(v in string for v in self.VN):
            for v in string:
                if v in self.VN:
                    string = string.replace(v, random.choice(self.P[v]), 1)
        return string

    def to_finite_automaton(self) -> FiniteAutomaton:
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

    def compute_type(self) -> str:
        """Computes the type of the grammar and returns it as a string value from GrammarTypology enum."""
        is_context_free, is_right_linear, is_left_linear, is_regular = True, False, False, True

        for key, productions in self.P.items():
            for production in productions:
                # Checking for RECURSIVELY_ENUMERABLE_GRAMMAR conditions.
                if len(key) > len(production) or (len(key) > 1 and any(char in self.VN for char in key)):
                    return GrammarTypology.RECURSIVELY_ENUMERABLE_GRAMMAR.value

                # Checking if not context-free or regular.
                if len(key) != 1 or key not in self.VN:
                    is_context_free, is_regular = False, False

                # Further checks if it's still considered regular.
                if is_regular:
                    if all(symbol in self.VT for symbol in production):
                        continue  # Still possibly right or left linear.
                    elif production[-1] in self.VN and all(symbol in self.VT for symbol in production[:-1]):
                        is_right_linear = True
                    elif production[0] in self.VN and all(symbol in self.VT for symbol in production[1:]):
                        is_left_linear = True
                    else:
                        is_regular = False

        # Determining the specific grammar type based on flags.
        if is_regular:
            if is_right_linear and not is_left_linear:
                return GrammarTypology.RIGHT_LINEAR_GRAMMAR.value
            elif is_left_linear and not is_right_linear:
                return GrammarTypology.LEFT_LINEAR_GRAMMAR.value
        if is_context_free:
            return GrammarTypology.CONTEXT_FREE_GRAMMAR.value
        
        return GrammarTypology.CONTEXT_SENSITIVE_GRAMMAR.value
    
    def to_dict(self) -> dict:
        """Method to export the Grammar to a dictionary format."""
        grammar_dict = {
            "VN": self.VN,
            "VT": self.VT,
            "P": self.P,
            "S": self.S,
        }
        return grammar_dict