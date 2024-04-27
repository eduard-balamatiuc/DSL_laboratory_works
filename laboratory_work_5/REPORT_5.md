# Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Eduard Balamatiuc

----

## Theory
In formal language theory, a context-free grammar, G, is said to be in Chomsky normal form (first described by Noam Chomsky) if all of its production rules are of the form:

A → BC,   or
A → a,   or
S → ε,

where A, B, and C are nonterminal symbols, the letter a is a terminal symbol (a symbol that represents a constant value), S is the start symbol, and ε denotes the empty string. Also, neither B nor C may be the start symbol, and the third production rule can only appear if ε is in L(G), the language produced by the context-free grammar G.


## Objectives:

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.


## Implementation description

I split my implementation of the chomsky normal form normalization into five parts, more details in short on the steps can be found on the Neso Academy video, really great explanation was provided there[2]

The 5 main steps are:
1. Checking the start symbol
2. Removing Null Productions
3. Removing Unit Productions
4. Removing Two or More Symbols on the Right Hand Side
5. Removing terminal and variable productions

I implemented each of the steps in a separated function just to make the code more readable and easier to test afterwards.

### 1. Checking the start symbol
Let's start of with the first part of my implementation which is the start symbol check. The function is called `check_start_symbol` and the main idea behind it is that we want to see if the start symbol appears in any of the right hand side of the productions. If it does appear, then we will create a new start symbol and add a new production rule to the grammar. The function modifies the grammar in the class.

Here is the implementation:
```python
    def start_symbol_check(self):
        """Method to check if the start symbol occurs on some right side of the productions.
        If it does, a new start symbol is created.
        """
        if self.S in "".join([element for value_list in self.P.values() for element in value_list]):
            new_start = f"{self.S}'"
            self.VN.add(new_start)
            self.P[new_start] = [self.S]
            self.S = new_start

```

### 2. Removing Null Productions

The next part was about removing the null productions. The function is called `remove_null_productions` and the main idea behind it is to remove all the null productions from the grammar and at the same time update all the affected productions, that is done by using a function that I implemented called `replace_all_combinations` that makes sure to provide all possible combinations when a string contains multiple characters that we want to remove because of the null production.

Below you can see the implementation of the `replace_all_combinations` function:

```python
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
```

It's expected behaviour would look something like this:
        
replace_all_combinations("ABC", "B") -> ["AC"]
replace_all_combinations("ABA", "A") -> ["AB", "B", "BA]
replace_all_combinations("AB", "C") -> ["AB"]
replace_all_combinations("ABABAB", "B") -> ["AABAB", "ABAAB", "ABABA", "AAAB", "ABAA", "AABA", "AAA"]
replace_all_combinations("ABBAB", "B") -> ["ABAB", "AAB", "ABBA", "AA"]

And of course here is the actual `remove_null_productions` function that does the main job by utilizing the `replace_all_combinations` function:

```python
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
```

### 3. Removing Unit Productions

Next element of the process is removing unit productions, which basically has the aim of getting rid of the cases in which we have a one to one mapping of the variables. This was done throught the function `remove_unit_productions` and in combination with the `compute_unit_productions` which is a function that I created to check if there are any other cases left so that it will iterate until it is finished. The unit productions that are being removed are stored backwards in the other production rules that are related to.

Below is the implementation of the `compute_unit_productions` function:

```python
    def compute_unit_productions(self):
        """Method to compute unit productions."""
        unit_productions = {v for v in self.VN if any(len(p) == 1 and p in self.VN for p in self.P[v])}
        return unit_productions
```

And here is the implementation of the `remove_unit_productions` function:

```python
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
```
As you can see above, if a case is found all it's right side actions will be transferred to the other production rules that are related to it.

### 4. Removing Two or More Symbols on the Right Hand Side

The next step was to find and udpate the predictions that had more than two symbols, and this was done by iterating other the possible available cases and in case one is found it creates a new state in which it stores the combination and it afterewards updates the other production rules that are related to it. This is done through a mapping dictionary that keeps in mind all the found cases along with the new states that are created.
The first part of the function, we actually find this new states and create them, and in the second part of the function we update all the elements of the grammar based on the found states.

Below is the implementation of the function `remove_two_or_more_symbols`:

```python
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
```

### 5. Removing terminal and variable productions

Last step of the process is removing any terminal and variable productions that are left in the grammar. This is done by iterating the starting keys of the production rules and in case a production rule has a termnial and a variable in it then we create a new state in case there is not one yet and we update the other production rules that are related to it.

Below is the implementation of the function `remove_terminal_and_variable_productions`:

```python

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
```

## Conclusions / Screenshots / Results

To conclude this laboratory work, I have implemented a method that normalizes a context-free grammar to Chomsky Normal Form. The implementation is encapsulated in a class and the normalization is done in five steps: checking the start symbol, removing null productions, removing unit productions, removing productions with more than two symbols, and removing terminal and variable productions. The implementation was tested on a sample grammar and also the functions are unit tested to validate the functionality of the project. Nevertheless the implementation provided is not perfect and can be improved, but it does the job for the context and it can accept any grammar, not only the one from the student's variant.

## References
[1] [Chomsky Normal Form Wiki](https://en.wikipedia.org/wiki/Chomsky_normal_form)
[2] [Conversion of CFG to Chomsky Normal Form](https://www.youtube.com/watch?v=FNPSlnj3Vt0&ab_channel=NesoAcademy)
