def read_grammar():
    try:
        n_input = input("Enter number of productions: ").strip()
        n = int(n_input)
    except ValueError:
        print("❌ Error: Please enter a numeric value.")
        return {}

    grammar = {}
    print("Enter productions (e.g., E -> E + T | T)")
    
    count = 0
    while count < n:
        line = input(f"Production {count+1}: ").strip()
        if not line:
            continue
        
        # Flexibly find the separator
        separator = None
        for s in ["->", "→", "=>"]:
            if s in line:
                separator = s
                break
        
        if not separator:
            print("❌ Invalid format! Use '->' between Head and Body.")
            continue
            
        head, rhs = map(str.strip, line.split(separator))
        prods = [p.strip() for p in rhs.split("|")]
        
        if head not in grammar:
            grammar[head] = []
        
        for p in prods:
            if p not in grammar[head]:
                grammar[head].append(p)
        count += 1
        
    return grammar