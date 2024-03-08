class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.f = f

    def __str__(self):
        """Printable representation of the Finite Automaton"""
        return f"Finite Automaton: q={self.q}, sigma={self.sigma}, delta={self.delta}, q0={self.q0}, f={self.f}"
    
    def string_belong_to_language(self, inputString):
        currentState = self.q0
        for c in inputString:
            if c not in self.sigma:
                return False
            for transition in self.delta[currentState]:
                if c == transition[0]:
                    if len(transition) == 2:
                        currentState = transition[1]
                        break
                    else:
                        currentState = transition[0]
        return currentState in self.f
    
    def to_regular_grammar(self):
        """Method for converting the finite automaton to a regular grammar."""
        VN = self.q
        VT = self.sigma
        P = {}
        for key in self.delta.keys():
            P[key] = [item[0] if len(item) == 1 else "".join(item) for item in self.delta[key]]
        S = self.q0
        grammar_dict = {
            "VN": VN,
            "VT": VT,
            "P": P,
            "S": S,
        }
        return grammar_dict
 
    def to_dict(self):
        """Method for exporting the finite automaton to a dictionary format."""
        return {
            "q": sorted(self.q),
            "sigma": sorted(self.sigma),
            "delta": sorted(self.delta),
            "q0": sorted(self.q0),
            "f": sorted(self.f),
        }

    def is_deterministic(self):
        """Method that checks if the finite automaton is deterministic."""
        for transition in self.delta.values():
            if len(set([item[0] for item in transition])) != len(transition):
                return False
                
        return True
    
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
print(test_finite_automaton.to_dfa())