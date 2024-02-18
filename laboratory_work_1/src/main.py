from grammar import Grammar

def main():
    VN = {'S', 'P', 'Q'}
    VT = {'a', 'b', 'c', 'd', 'e', 'f'}
    P = {
        'S': ['aP', 'bQ'],
        'P': ['bP', 'cP', 'dQ', 'e'],
        'Q': ['eQ', 'fQ', 'a']
    }
    S = 'S'
    grammar = Grammar(VN, VT, P, S)
    print("Generated strings:")
    for _ in range(5):
        print(grammar.generate_string())
    
    fa = grammar.to_finite_automaton()
    test_string = "ace" 
    print(f"Does '{test_string}' belong to the language? {fa.string_belong_to_language(test_string)}")

if __name__ == "__main__":
    main()    
