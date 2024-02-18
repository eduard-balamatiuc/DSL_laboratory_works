# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Eduard Balamatiuc

----

## Theory
If needed, but it should be written by the author in her/his words.


## Objectives:

1. Discover what a language is and what it needs to have in order to be considered a formal one;

2. Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

    a. Create GitHub repository to deal with storing and updating your project;

    b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like setting up the project, launching it correctly and etc.);

    c. Store reports separately in a way to make verification of your work simpler (duh)

3. According to your variant number, get the grammar definition and do the following:

    a. Implement a type/class for your grammar;

    b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

    c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

    d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description

- Grammar Class: Encapsulates the components of a grammar, including non-terminals, terminals, production rules, and the start symbol. It includes a method to generate valid strings and a method to transform the grammar into a finite automaton.

```python
import random
from finite_automaton import FiniteAutomaton

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
    
    def generate_string(self):
        string = self.S
        while any(v in string for v in self.VN):
            for v in string:
                if v in self.VN:
                    string = string.replace(v, random.choice(self.P[v]), 1)
        return string
    
    def to_finite_automaton(self):
        q = self.VN
        sigma = self.VT
        q0 = self.S
        delta = {}
        for key in self.P.keys():
            delta[key] = [(item[0],) if len(item) == 1 else (item[0], item[1]) for item in self.P[key]]
        values = [item for sublist in self.P.values() for item in sublist]
        f = [item for item in values if len(set([key for key in self.P.keys()])-set(item)) == len(set([key for key in self.P.keys()]))]
        return FiniteAutomaton(q, sigma, delta, q0, f)
```

- Finite Automaton Class: Represents a finite automaton with states, alphabet, transition functions, a start state, and accept states. It includes a method to check if a given string belongs to the language defined by the automaton.

```python
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
            for transition in self.delta[currentState]:
                if c == transition[0]:
                    if len(transition) == 2:
                        currentState = transition[1]
                        break
                    else:
                        currentState = transition[0]
        return currentState in self.f
```

## Conclusions / Screenshots / Results
To conclude, the implementation of the Grammar and FiniteAutomaton classes was successful. The Grammar class is able to generate valid strings from the language expressed by the given grammar, and the FiniteAutomaton class is able to check if a given string belongs to the language defined by the automaton.

## References
 - Fromal Language and Finite Automata guide for practical lessons
 - https://www.youtube.com/watch?v=Qa6csfkK7_I&list=PLLOaAE6VrtlRu6VI7gKVd9fw9ONRL3LJx&index=1&ab_channel=NesoAcademy
 - https://www.youtube.com/watch?v=40i4PKpM0cI&list=PLLOaAE6VrtlRu6VI7gKVd9fw9ONRL3LJx&index=3&ab_channel=NesoAcademy