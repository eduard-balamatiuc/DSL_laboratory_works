# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata
### Author: Eduard Balamatiuc

----

## Theory
### Finite Automata 
Automata theory is the study of abstract computational devices (abstract state machine). An automaton is an abstract model of a digital computer. As such, every automaton includes some essential features. It has a mechanism for reading input. It will be assumed that the input is a string over a given alphabet. The input mechanism can read the input string from left to right, one symbol at a time and it can be detected the end of the string. The automaton can produce the output of some form and has a control unit, which can be in any one of a finite number of internal states, and which can change state in some defined manner based on transition functions. 

The finite automaton (FA) is characterized by the finite number of states and it is known the following types of the FA: 
- Deterministic finite automaton (DFA). 
- Nondeterministic finite automaton (NFA).  
- λ - Nondeterministic finite automaton (λ–NFA). 

### Deterministic Finite Automaton (DFA)
A deterministic finite automaton is a 5-tuple (Q, Σ, δ, q0, F) where: 
- Q is a finite set of states.
- Σ is an input alphabet.
- δ is a transition function, δ: Q × Σ → Q.
- q0 is the intial state.
- F is a set of final states.

### Nondeterministic Finite Automaton (NFA)
A nondeterministic finite automaton is a 5-tuple (Q, Σ, δ, q0, F) where:
- Q is a finite set of states.
- Σ is an input alphabet.
- δ is a transition function, δ: Q × Σ → 2^Q.
- q0 is the intial state.
- F is a set of final states.

**Differences from the DFA:**
- transition function δ can go into several states.
- it can have λ-transitions.

### Chomsky Hierarchy
The Chomsky hierarchy is a classification of formal grammars, each of which generates a class of formal languages. It is named after its creator, Noam Chomsky. The Chomsky hierarchy is a containment hierarchy of classes of formal grammars. Each class of grammar generates a class of formal languages. The hierarchy is based on the expressive power of the grammar. The Chomsky hierarchy is a powerful tool for understanding the capabilities and limitations of different classes of formal grammars and formal languages.

The Chomsky hierarchy consists of four classes of formal grammar:
- Type 0: Recursively enumerable grammar.
- Type 1: Context-sensitive grammar.
- Type 2: Context-free grammar.
- Type 3: Regular grammar.
    - Right-linear grammar.
    - Left-linear grammar.

## Objectives:
1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
    a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

    b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

    a. Implement conversion of a finite automaton to a regular grammar.

    b. Determine whether your FA is deterministic or non-deterministic.

    c. Implement some functionality that would convert an NDFA to a DFA.
    
    d. Represent the finite automaton graphically (Optional, and can be considered as a __*bonus point*__):
      
    - You can use external libraries, tools or APIs to generate the figures/diagrams.
        
    - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

Please consider that all elements of the task 3 can be done manually, writing a detailed report about how you've done the conversion and what changes have you introduced. In case if you'll be able to write a complete program that will take some finite automata and then convert it to the regular grammar - this will be **a good bonus point**.


## Implementation description

- For the first task of this laboratory work I have implemented a method in the Grammar class that classifies the grammar based on the Chomsky hierarchy. The method returns a string that represents the type of the grammar.

I created a new class for the grammar type definition to be more explicit and to have a better understanding of the code. The class has the following structure:

```python
class GrammarTypology(str, Enum):
    """Enum class for the different types of grammars. 
    The values are the same as the ones used in the Chomsky hierarchy based on the LFPC Guide.
    """
    RECURSIVELY_ENUMERABLE_GRAMMAR = "type_0"
    CONTEXT_SENSITIVE_GRAMMAR = "type_1"
    CONTEXT_FREE_GRAMMAR = "type_2"
    RIGHT_LINEAR_GRAMMAR = "type_3_right"
    LEFT_LINEAR_GRAMMAR = "type_3_left"
```

Then inside the Grammar class that I previously implemented in the first laboratory work, I added the following method:

```python
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
```
The behind logic of the method is basically to assume that the grammar is regular and is context free and then to check for the conditions that would make it not regular or not context free. We iterate through the production and on each "transition" we check if the grammar is of the first type 0, otherwise we check if it's context free, regular, and if it's still regular we check if it's right or left linear by making sure that the first or the last elements are a part of the non-terminal set and the rest of the elements are part of the terminal set. Lastly, we return the type of the grammar based on the flags that we set during the iteration.

- For the second task of this laboratory work I have implemented a method in the FiniteAutomaton class that converts the finite automaton to a regular grammar. The method returns a Grammar object.

```python
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
```
The behind idea is quite simple, it was the reversed operation of the grammar to finite automaton conversion. We iterate through the transition function keeping the same keys and only creating a join of the tuple structure if the length of the tuple is greater than 1, otherwise we would put the single element of the tuple in place. Then we return the dictionary that represents the grammar.

- For the third task of this laboratory work I have implemented a method in the FiniteAutomaton class that checks if the finite automaton is deterministic or non-deterministic. The method returns a boolean value.

```python
    def is_deterministic(self):
        """Method that checks if the finite automaton is deterministic."""
        for transition in self.delta.values():
            if len(set([item[0] for item in transition])) != len(transition):
                return False
                
        return True
```
The behind logic that I applied is to iterate other each list of transitions for each of the keys and check if the length of the set of the first elements of the tuples is equal to the length of the list of transitions. If it's not equal then it's non-deterministic, otherwise it's deterministic since we would have unique inputs for each of the transitions.

- For the fourth task of this laboratory work I have implemented a method in the FiniteAutomaton class that converts a non-deterministic finite automaton to a deterministic finite automaton. The method returns a FiniteAutomaton object.

```python
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
```
The behind logic of the method is to create a new dictionary that will map the new states of the DFA to the old states of the NFA. Then we create a new dictionary for the transition function of the DFA and we create a new set of final states for the DFA. We iterate through the unexplored states and for each of the input symbols we find the next states that are reachable from the current state set under the input symbol. If the next state set is not in the new states dictionary we add it and we append it to the unexplored list. Then we check if the current state set includes any NFA final states and if it does we add it to the set of final states of the DFA. Lastly, we convert the set of states back to a list format for compatibility and we return the new DFA.

- For the fifth task of this laboratory work I have implemented a method in the FiniteAutomaton class that represents the finite automaton graphically. I used the graphviz library to generate the graph of the finite automaton.

```python
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
```
For this task I used the graphviz library to generate the graph of the finite automaton. I added the states and the transitions to the graph and I marked the initial state. Then I returned the graph.

- Additional stuff
I also added a magic method for both grammar an finite automaton classes to be able to print the objects in a more readable way.

Another addition was the dictionary export method for both classes, this allowed for easy testing of the methods and for easy visualization of the objects.

Nevertheless all tasks were tested using unit tests and the results were as expected.
I added a file for each of the classes, and each of them contain multiple classes with tests for the methods of the classes.
- `test_grammar.py`
- `test_finite_automaton.py`

## Conclusions / Screenshots / Results
To conclude, the implementation of the Grammar and FiniteAutomaton classes was successful. The Grammar class is able to generate valid strings from the language expressed by the given grammar, and the FiniteAutomaton class is able to check if a given string belongs to the language defined by the automaton. The Grammar class is also able to classify the grammar based on the Chomsky hierarchy and the FiniteAutomaton class is able to convert the finite automaton to a regular grammar, to check if the finite automaton is deterministic or non-deterministic, to convert a non-deterministic finite automaton to a deterministic finite automaton, and to represent the finite automaton graphically.

## References
 - Fromal Language and Finite Automata guide for practical lessons
 - https://www.youtube.com/watch?v=i-fk9o46oVY&ab_channel=NesoAcademy
 - https://www.python.org/doc/