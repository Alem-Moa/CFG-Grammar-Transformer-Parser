# CFG Grammar Transformer & Parser

A Python-based tool to analyze Context-Free Grammars (CFG), eliminate parsing obstacles, and generate FIRST/FOLLOW sets.

## 🚀 Features
- **Left Recursion Removal:** Converts direct left recursion into right recursion to prevent infinite loops in top-down parsers.
- **Left Factoring:** Extracts common prefixes to resolve non-determinism.
- **Set Calculation:** Computes **FIRST** and **FOLLOW** sets for all non-terminals.
- **LL(1) Analysis:** Checks for grammar compatibility with predictive parsers.

## 📁 Project Structure
- `left_recursion.py and left_factoring.py`: Logic for Left Recursion and Factoring.
- `first_follow.py`: Algorithm for FIRST/FOLLOW sets.
- `ll1_parser.py`: Table generation logic.

## 🛠️ Implementation Challenges
The main challenge was handling **Epsilon ($\epsilon$)** transitions during the FOLLOW set calculation.
Since a non-terminal can derive an empty string, the algorithm must "look ahead" through the production string until it finds a non-nullable symbol.

## How to Use
1. Run `python main.py`.
2. Enter the number of productions.
3. Input rules in the form `A -> alpha | beta`.
4. Provide a space-separated string to parse.
