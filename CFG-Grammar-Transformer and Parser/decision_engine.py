from left_recursion import detect_left_recursion
from left_factoring import detect_left_factoring
from first_follow import compute_first, compute_follow, display_sets
from ll1_parser import ll1_parse
from slr1_parser import slr1_parse

def decide_parser(grammar):
    # Check if grammar was read successfully
    if not grammar:
        print("\n❌ Error: Grammar is empty. Please check your input format.")
        return

    print("\n[Decision Engine]")

    # 1. Detect left recursion
    direct, indirect = detect_left_recursion(grammar)
    print("\n--- LEFT RECURSION ---")
    if not direct and not indirect:
        print("No left recursion detected ✓")
    else:
        if direct:
            print(f"Direct left recursion detected in: {direct}")
        if indirect:
            print(f"Indirect left recursion detected in: {indirect}")

    # 2. Detect left factoring
    left_factoring = detect_left_factoring(grammar)
    print("\n--- LEFT FACTORING ---")
    if not left_factoring:
        print("No left factoring detected ✓")
    else:
        for head, conflicts in left_factoring.items():
            print(f"Non-terminal '{head}' has conflicts: {conflicts}")

    # 3. Compute and Display FIRST and FOLLOW sets
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    display_sets(first, follow)

    # 4. Determine Parser Type
    # LL(1) cannot have left recursion OR left factoring
    is_ll1 = not direct and not indirect and not left_factoring

    # Ask for input string here so it's ready for whichever parser is chosen
    input_string = input("\nEnter string to parse (use spaces between tokens): ").strip()

    if is_ll1:
        print("\n✅ Grammar is LL(1) compatible. Launching LL(1) Non-Recursive Parser...")
        ll1_parse(grammar, input_string)
    else:
        print("\n⚠️ Grammar is NOT LL(1) (Recursion/Factoring found). Falling back to SLR(1) Parser...")
        slr1_parse(input_string, grammar)