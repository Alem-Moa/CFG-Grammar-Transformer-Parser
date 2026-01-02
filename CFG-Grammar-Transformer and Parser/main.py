from grammar import read_grammar
from decision_engine import decide_parser

def main():
    print("=== LL(1) and SLR(1) Parser Tool ===")
    grammar = read_grammar()
    decide_parser(grammar)

if __name__ == "__main__":
    main()