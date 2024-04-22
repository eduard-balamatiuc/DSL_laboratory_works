import random
from collections import defaultdict

class Grammar:
    """Class representing a generalized grammar."""
    def __init__(self, VN, VT, P, S="S"):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S

    def __str__(self):
        """Printable representation of the grammar."""
        rules = [f"{v} -> {', '.join(self.P[v])}" for v in self.P]
        return f"Grammar:\nVN={self.VN}\nVT={self.VT}\nP={rules}\nS={self.S}"

    def to_dict(self) -> dict:
        """Method to export the Grammar to a dictionary format."""
        grammar_dict = {
            "VN": self.VN,
            "VT": self.VT,
            "P": self.P,
            "S": self.S,
        }
        return grammar_dict
    
    def start_symbol_check(self):
        """Method to check if the start symbol occurs on some right side of the productions.
        If it does, a new start symbol is created."""
        if self.S in "".join([element for value_list in self.P.values() for element in value_list]):
            new_start = f"{self.S}'"
            self.VN.add(new_start)
            self.P[new_start] = [self.S]
            self.S = new_start


    def normalize_to_chomsky_normal_form(self):
        """Method to normalize to Chomsky Normal Form."""
        self.start_symbol_check()
        self.remove_null_productions()
        # self._eliminate_renaming()
        # self._eliminate_inaccessible_symbols()
        # self._eliminate_non_productive_symbols()
        # self._convert_to_chomsky_normal_form()

if __name__ == "__main__":
    # Example usage
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
    grammar = Grammar(VN, VT, P)
    print("Original Grammar:")
    print(grammar.to_dict())

    grammar.normalize_to_chomsky_normal_form()
    print("Chomsky Normal Form:")
    print(grammar.to_dict())
