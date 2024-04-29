from graphviz import Digraph
from parser_class import Parser
from lexer import Lexer

def main():
    # Input or update the text according to your needs
    input_text = "723 + 3 * (120 / (12 / (3 + 1) - 1))"
    lexer = Lexer(input_text)
    parser = Parser(lexer)
    ast = parser.parse()

    # Create a graph
    dot = Digraph()
    ast.graph(dot)  # Now it correctly handles the root case without a parent
    dot.render('output/out', format='png', view=True)  # Saves and opens the graph as a PNG

if __name__ == "__main__":
    main()
