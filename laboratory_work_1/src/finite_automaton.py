class FiniteAutomaton:
    def __init__(self, q, sigma, delta, q0, f):
        self.q = q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.f = f
    
    def string_belong_to_language(self, inputString):
        print(f"Checking if '{inputString}' belongs to the language...")
        print(f"self.q: {self.q}, self.sigma: {self.sigma}, self.delta: {self.delta}, self.q0: {self.q0}, self.f: {self.f}")
        currentState = self.q0
        for c in inputString:
            if c not in self.sigma:
                return False
            if c in 
        return currentState in self.f