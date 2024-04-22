import random
from enum import Enum


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
    
    def to_dict(self) -> dict:
        """Method to export the Grammar to a dictionary format."""
        grammar_dict = {
            "VN": self.VN,
            "VT": self.VT,
            "P": self.P,
            "S": self.S,
        }
        return grammar_dict


if __name__=="__main__":
    # Example usage
    VN = {"S", "A", "B", "C", "D", "E"}
    VT = {"a", "b"}
    P = {
        "S": ["aB", "AC"],
        "A": ["a", "ASC", "BC", "aD"],
        "B": ["b", "bS"],
        "C": ["ε", "BA"],
        "E": ["aB"],
        "D": ["abC"]
    }
    grammar = Grammar(VN, VT, P)

    