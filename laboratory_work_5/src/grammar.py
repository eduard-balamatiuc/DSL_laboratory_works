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
        If it does, a new start symbol is created.
        """
        if self.S in "".join([element for value_list in self.P.values() for element in value_list]):
            new_start = f"{self.S}'"
            self.VN.add(new_start)
            self.P[new_start] = [self.S]
            self.S = new_start

    def replace_all_combinations(self, value, node):
        """Method that given a possible value and a node, removes the node from the value in all possibl combinations
        and returns the new values.
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

    def compute_unit_productions(self):
        """Method to compute unit productions."""
        unit_productions = {v for v in self.VN if any(len(p) == 1 and p in self.VN for p in self.P[v])}
        return unit_productions

    def remove_unit_productions(self):
        """Method to remove unit productions from the grammar."""
        while self.compute_unit_productions():
            # replace the unit productions identified to the right side of the productions
            unit_productions = self.compute_unit_productions()
            for key in unit_productions:
                for production in self.P[key]:
                    if len(production) == 1 and production in self.VN:
                        self.P[key].remove(production)
                        self.P[key].extend(self.P[production])

    def remove_two_or_more_symbols(self):
        """Method to remove productions with more than 2 symbols."""
        # extract violating productions
        violating_productions = {v: [p for p in self.P[v] if len(p) > 2] for v in self.P}
        new_productions = defaultdict(list)
        for v in violating_productions:
            for production in violating_productions[v]:
                last_two = production[-2:]
                if last_two not in new_productions:
                    new_state = f"{v}*"
                    self.VN.add(new_state)
                    new_productions[last_two].append(new_state)
                    self.P[new_state] = [last_two]
        # replace the violating productions with the new productions
        for production in new_productions:
            for v in self.P:
                for p in self.P[v]:
                    if (p[-2:] == production) and (len(p) > 2):
                        self.P[v].remove(p)
                        p = p[:-2] + new_productions[production][0]
                        self.P[v].append(p)

    def remove_terminal_and_variable_productions(self):
        """Method to remove terminal and variable productions."""
        # fina all terminal symbols to be replaced
        states_to_iterate = [key for key in self.P.keys()]
        for v in states_to_iterate:
            for i, production in enumerate(self.P[v]):
                if (len(production) > 1) and (production.upper() != production) and (production.lower() != production):
                    for symbol in production:
                        if symbol in self.VT:
                            new_state = f"{symbol}*"
                            if new_state not in self.VN:
                                self.VN.add(new_state)
                                self.P[new_state] = [symbol]
                            self.P[v][i] = production.replace(symbol, new_state)

    def normalize_to_chomsky_normal_form(self):
        """Method to normalize to Chomsky Normal Form."""
        print("Start Symbol Check:")
        self.start_symbol_check()
        print("Remove Null Productions:")
        self.remove_null_productions()
        print("Remove Unit Productions:")
        self.remove_unit_productions()
        print("Remove Two or More Symbols:")
        self.remove_two_or_more_symbols()
        print("Remove Terminal and Variable Productions:")
        self.remove_terminal_and_variable_productions()

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

