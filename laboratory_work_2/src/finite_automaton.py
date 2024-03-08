from graphviz import Digraph


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
        """Method for checking if a string belongs to the language of the finite automaton."""
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
    
    def to_dfa(self):
        """Method for converting the finite automaton to a deterministic finite automaton."""
        if self.is_deterministic():
            return self
        
        new_states = {frozenset([self.q0]): self.q0}  # Mapping from NFA state sets to DFA state names
        new_delta = {}
        dfa_start_state = frozenset([self.q0])
        unexplored = [dfa_start_state]
        dfa_final_states = set()

        while unexplored:
            current_state_set = unexplored.pop()
            for input_symbol in sorted(self.sigma):
                # Find all NFA states reachable from the current state set under the input symbol
                next_states = set()
                for state in current_state_set:
                    transitions = self.delta.get(state, [])
                    for symbol, next_state in transitions:
                        if symbol == input_symbol:
                            next_states.add(next_state)

                if next_states:
                    next_state_set = frozenset(next_states)
                    if next_state_set not in new_states:
                        new_states[next_state_set] = str(len(new_states))
                        unexplored.append(next_state_set)
                    # Record the transition in the DFA
                    new_delta.setdefault(new_states[current_state_set], []).append((input_symbol, new_states[next_state_set]))

            # Check if the current state set includes any NFA final states
            if any(state in self.f for state in current_state_set):
                dfa_final_states.add(new_states[current_state_set])

        # Convert set of states back to a list format for compatibility
        new_q = set(new_states.values())
        new_f = list(dfa_final_states)

        return FiniteAutomaton(new_q, self.sigma, new_delta, new_states[dfa_start_state], new_f)
        
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
    
    def visualize(self):
        """Method for visualizing the finite automaton."""
        dot = Digraph()

        # Add states
        for state in self.q:
            if state in self.f:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')

        # Mark the initial state
        dot.node('', shape='none')
        dot.edge('', self.q0)

        # Add edges
        for src, transitions in self.delta.items():
            for input_symbol, dest in transitions:
                dot.edge(src, dest, label=input_symbol)

        return dot
