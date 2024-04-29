# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Eduard Balamatiuc

----

## Theory
Parsing, syntax analysis, or syntactic analysis is the process of analyzing a string of symbols, either in natural language, computer languages or data structures, conforming to the rules of a formal grammar. The term parsing comes from Latin pars (orationis), meaning part (of speech).

The term has slightly different meanings in different branches of linguistics and computer science. Traditional sentence parsing is often performed as a method of understanding the exact meaning of a sentence or word, sometimes with the aid of devices such as sentence diagrams. It usually emphasizes the importance of grammatical divisions such as subject and predicate.

An abstract syntax tree (AST) is a data structure used in computer science to represent the structure of a program or code snippet. It is a tree representation of the abstract syntactic structure of text (often source code) written in a formal language. Each node of the tree denotes a construct occurring in the text. It is sometimes called just a syntax tree.

The syntax is "abstract" in the sense that it does not represent every detail appearing in the real syntax, but rather just the structural or content-related details. For instance, grouping parentheses are implicit in the tree structure, so these do not have to be represented as separate nodes. Likewise, a syntactic construct like an if-condition-then statement may be denoted by means of a single node with three branches.

This distinguishes abstract syntax trees from concrete syntax trees, traditionally designated parse trees. Parse trees are typically built by a parser during the source code translation and compiling process. Once built, additional information is added to the AST by means of subsequent processing, e.g., contextual analysis.

Abstract syntax trees are also used in program analysis and program transformation systems.

## Objectives:

1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description

In this laboratory work, there are 3 main parts that I've worked on:
1. Updating the previous Lexer implementation from the 3rd laboratory work.
2. Implementing the Abstract Syntax Tree (AST) data structure.
3. Implementing the Parser.

### 0. How to run the code
To run and test the implementation I've created a `main.py` file that can be used to test the implementation. The file can be run using the following command:
```bash
python main.py
```
If you want to test on different inputs, you can change the `input_text` variable in the `main.py` file and run the file again.


### 1. Lexer implementation
In the laboratory work 3, my implementation was using simple string manipulation to extract the tokens from the input text. In this laboratory work, I've updated the implementation to use regular expressions to identify the type of the token. I still kept the idea of having a `Token` class that has a `type` and a `value` field. and The Lexer working with arithmetical expressions. but now everything is much cleaner and compact.
The main updates that happened were for the `tokenize` method and `get_next_token` method. They can be seen below.

```python
    def tokenize(self):
        """Tokenize the entire input text using regular expressions."""
        token_specification = [
            ('INTEGER',   r'\d+'),            # Integer
            ('PLUS',      r'\+'),             # Plus sign
            ('MINUS',     r'-'),              # Minus sign
            ('MUL',       r'\*'),             # Multiplication sign
            ('DIV',       r'\/'),             # Division sign
            ('LPAREN',    r'\('),             # Left Parenthesis
            ('RPAREN',    r'\)'),             # Right Parenthesis
            ('WHITESPACE', r'\s+'),           # Whitespace
            ('UNKNOWN',   r'.'),              # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'WHITESPACE':
                continue
            elif kind == 'INTEGER':
                value = int(value)
            elif kind == 'UNKNOWN':
                raise Exception(f'Unexpected character: {value}')
            self.tokens.append(Tokenner(TokenType[kind], value))
        self.tokens.append(Tokenner(TokenType.EOF, None))
```

```python
    def get_next_token(self):
        """Return the next token from the token list."""
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        else:
            return Tokenner(TokenType.EOF, None)
```

### 2. Abstract Syntax Tree (AST) implementation
The next step in the laboratory work was the implementation of the data structurer for the Abstract Syntax Tree. I've created a main class called ASTNode which has a method `graph` that will be used afterwards by both child classes BinOp and Num. The BinOp class is used to represent binary operations like addition, subtraction, multiplication, and division. The Num class is used to represent the integer values. The ASTNode class has a method `graph` that will be used to print the tree in a graphical way.
The classes are used to provide more structure to the AST and while at the same time saving the values and the mapping between the nodes.

Below can be found the implementation of the three classes:

```python
class ASTNode:
    def graph(self, graph, parent_name=None):
        pass

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def graph(self, graph, parent_name=None):
        """Recursively create a graph of the AST using the graphviz library."""
        # Define a unique name for this operator based on its memory id to avoid collisions
        operator_name = f'op_{id(self)}'
        graph.node(operator_name, label=str(self.op.value))
        
        # Connect this node with its parent node, if a parent exists
        if parent_name:
            graph.edge(parent_name, operator_name)

        # Recursively call graph on left and right children
        self.left.graph(graph, operator_name)
        self.right.graph(graph, operator_name)

class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def graph(self, graph, parent_name=None):
        """Create a graph of the AST using the graphviz library."""
        # Define a unique name for this number based on its memory id to avoid collisions
        node_name = f'num_{id(self)}'
        graph.node(node_name, label=str(self.value))
        
        # Connect this node with its parent node, if a parent exists
        if parent_name:
            graph.edge(parent_name, node_name)
```

### 3. Parser implementation
This was the last step in the laboratory work. This class has a couple of main methods that we will go through:
1. `parse` 
2. `expr`
3. `term`
4. `factor`
5. `eat`
6. `error`

##### 1. `parse` method
This is the main method of the class that does practically nothing, you know the interview with the Technical Director of OpenAI when he was asked what data are they using and he said I don't know, exactly the Director took the credit of the work of the team. This is the same case here, the `parse` method is the Director, it just calls the `expr` method and returns the result.

```python
    def parse(self):
        """Parse the input text."""
        return self.expr()
```

##### 2. `expr` method
Since we were talking about expr, let's see what this part was doing. The `expr` method is used to parse the expression. It calls the `term` (which is actually another fictive worker at OpenAI that does the behind job while `expr` takes the credit for it) method and then it checks if the next token is a `PLUS` or `MINUS` token. If it is, it creates a new BinOp node and calls the `term` method again. It does this until there are no more `PLUS` or `MINUS` tokens.

```python
    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node
```

##### 3. `term` method
Sincce we mentioned the `term` method before, don't think that he is the hard working guy in the team which everyone takes credit of him, actually no, he is also one of them. The `term` method is used to parse the term. It calls the `factor`(which is another fictive worker at OpenAI tht does the behind job while `term` takes the credit for it) method and then it checks if the next token is a `MUL` or `DIV` token. If it is, it creates a new BinOp node and calls the `factor` method again. It does this until there are no more `MUL` or `DIV` tokens.

```python
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node
```

##### 4. `factor` method
The `factor` method is used to parse the factor. If the current token is an `INTEGER` token, it creates a new Num node and returns it. If the current token is an `LPAREN` token, it eats the `LPAREN` token, parses the expression, and then eats the `RPAREN` token. Thankfully the `factor` method works actually really hard and does most of the job by itself, except with the eating element, but I mean, aren't we all eating at the end of the day?

```python
    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
```

##### 5. `eat` method
The `eat` method is one of the most used throughout the class and that is because it processes all the tokesh*t that it is given. It checks if the current token type is the same as the expected token type and if it is, it moves to the next token. If it is not, then it calls his friend `error` to help him out.

```python
    def eat(self, token_type):
        """Consume the current token if it matches the passed token type."""
        # Compare the current token type with the passed token type and consume it if they match
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
```

##### 6. `error` method
You know the triangle instrument from orchestra's, the one that in movies it's used at the end, it does only one thing and it's simple stupid. Well this is the `error` method, although it's not called at the end necessarily, it does only one thing, it raises an exception with the message "Invalid syntax".

```python
    def error(self):
        """Raise an exception if the current token is not the expected token."""
        raise Exception("Invalid syntax")
```

## Conclusions / Screenshots / Results
To conclude this laboratory work, I have updated the Lexer implementation from the 3rd laboratory work to use regular expressions to identify the type of the token. I have implemented the Abstract Syntax Tree (AST) data structure and the Parser. The parser is used to extract the syntactic information from the input text. The AST is used to represent the structure of the program or code snippet. The parser is used to parse the input text and build the AST. The AST is then used to represent the structure of the input text in a graphical way.

## References
[1] [Parsing Wiki](https://en.wikipedia.org/wiki/Parsing)

[2] [Abstract Syntax Tree Wiki](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
 