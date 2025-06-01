import json

def load_nfa_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def epsilon_closure(states, transitions):
    closure = set(states)
    stack = list(states)
    
    while stack:
        current_state = stack.pop()
        for transition_key, next_states in transitions.items():
            state, symbol = transition_key.split(',', 1)
            if state == current_state and symbol == 'ε':
                for next_state in next_states:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
    
    return closure

def move(current_states, symbol, transitions):
    next_states = set()
    
    for state in current_states:
        transition_key = f"{state},{symbol}"
        if transition_key in transitions:
            next_states.update(transitions[transition_key])
    
    return next_states

def simulate_nfa(states, alphabet, transitions, start_state, accept_states, input_string):
    print(f"String de intrare: '{input_string}'")
    print(f"Stare inițială: {start_state}")

    current_states = epsilon_closure({start_state}, transitions)
    print(f"Epsilon-closure inițial: {sorted(list(current_states))}")
    print("\nPașii de execuție:")
    
    for i, symbol in enumerate(input_string):
        if symbol not in alphabet:
            print(f"Eroare: Simbolul '{symbol}' nu face parte din alfabet!")
            return False
        
        print(f"\nPas {i+1}: Procesăm simbolul '{symbol}'")
        print(f"Stări curente: {sorted(list(current_states))}")

        moved_states = move(current_states, symbol, transitions)
        print(f"După move cu '{symbol}': {sorted(list(moved_states))}")

        current_states = epsilon_closure(moved_states, transitions)
        print(f"După epsilon-closure: {sorted(list(current_states))}")

        if not current_states:
            print("Nu mai avem stări active - string respins!")
            return False
    
    final_accept_states = current_states.intersection(set(accept_states))
    is_accepted = len(final_accept_states) > 0
    
    print(f"\nStări finale: {sorted(list(current_states))}")
    print(f"Stări de acceptare: {accept_states}")
    print(f"Stări finale de acceptare: {sorted(list(final_accept_states))}")
    print(f"String acceptat: {'DA' if is_accepted else 'NU'}")
    
    return is_accepted

def main():
    config = load_nfa_config('nfa_config.json')
    
    states = config['states']
    alphabet = config['alphabet']
    transitions = config['transitions']
    start_state = config['start_state']
    accept_states = config['accept_states']
    
    print("=== CONFIGURAȚIA NFA ===")
    print(f"Stări: {states}")
    print(f"Alfabet: {alphabet}")
    print(f"Stare inițială: {start_state}")
    print(f"Stări de acceptare: {accept_states}")
    print(f"Tranziții: {transitions}")
    print("\n" + "="*50 + "\n")

    test_strings = ["", "a", "ab", "aa", "abb", "aab", "abab"]
    
    for test_string in test_strings:
        print(f"\n{'='*20} TEST {'='*20}")
        result = simulate_nfa(states, alphabet, transitions, start_state, accept_states, test_string)
        print(f"Rezultat: {'ACCEPTAT' if result else 'RESPINS'}")
        print("="*50)

    print("\n=== MOD INTERACTIV ===")
    while True:
        user_input = input("\nIntroduceți un string pentru testare (sau 'quit' pentru ieșire): ")
        if user_input.lower() == 'quit':
            break
        
        print(f"\n{'='*20} TEST INTERACTIV {'='*20}")
        result = simulate_nfa(states, alphabet, transitions, start_state, accept_states, user_input)
        print(f"Rezultat: {'ACCEPTAT' if result else 'RESPINS'}")
        print("="*50)

if __name__ == "__main__":
    main()