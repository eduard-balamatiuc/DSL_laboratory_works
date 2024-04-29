from tokenner import TokenType

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

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        """Raise an exception if the current token is not the expected token."""
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        """Consume the current token if it matches the passed token type."""
        # Compare the current token type with the passed token type and consume it if they match
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

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

    def parse(self):
        """Parse the input text."""
        return self.expr()
