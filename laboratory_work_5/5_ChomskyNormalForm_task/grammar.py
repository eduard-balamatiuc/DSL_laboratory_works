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

    def replace_all_combinations(self, value, node):
        """Method that given a possible value and a node, removes the node from the value in all possibl combinations
        and returns the new values.
        
        replace_all_combinations("ABC", "B") -> ["AC"]
        replace_all_combinations("ABA", "A") -> ["AB", "B", "BA]
        replace_all_combinations("AB", "C") -> ["AB"]
        replace_all_combinations("ABABAB", "B") -> ["AABAB", "ABAAB", "ABABA", "AAAB", "ABAA", "AABA", "AAA"]
        replace_all_combinations("ABBAB", "B") -> ["ABAB", "AAB", "ABBA", "AA"]
        """
        if node not in value:
            # If the node is not in the value, return the original value in a list
            return [value]
        
        results = set()  # Using a set to avoid duplicate entries

        # Recursive function to generate combinations by removing the node
        def generate_combinations(current, start):
            # Loop through the string and try removing the node at each position
            for i in range(start, len(current)):
                if current.startswith(node, i):
                    # Remove the node and recursively call with the new string
                    new_combination = current[:i] + current[i + len(node):]
                    if new_combination not in results:
                        results.add(new_combination)
                        generate_combinations(new_combination, i)

        # Start generating combinations from the initial value
        generate_combinations(value, 0)

        # Convert the set to a list and ensure the original value is removed
        result_list = list(results)

        if value in result_list:
            result_list.remove(value)

        return result_list

    def remove_null_productions(self):
        """Method to eliminate ε productions from the grammar."""
        nullable = {v for v in self.VN if "" in self.P[v]}
        
        for node_with_empty in nullable:
            for v in self.VN:
                for production in self.P[v]:
                    if node_with_empty in production:
                        if production == node_with_empty:
                            nullable.add(v)
                        else:
                            new_productions = self.replace_all_combinations(production, node_with_empty)
                            self.P[v].extend(new_productions)
            self.P[node_with_empty] = [production for production in self.P[node_with_empty] if production != ""]




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
