import json

def load_dfa_config(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def simulate_dfa(states, alphabet, transitions, start_state, accept_states, input_string):
    current_state = start_state
    
    print(f"String de intrare: '{input_string}'")
    print(f"Stare inițială: {current_state}")
    print("\nPașii de execuție:")
    
    for i, symbol in enumerate(input_string):
        if symbol not in alphabet:
            print(f"Eroare: Simbolul '{symbol}' nu face parte din alfabet!")
            return False

        transition_key = f"{current_state},{symbol}"
        if transition_key not in transitions:
            print(f"Pas {i+1}: Din starea '{current_state}' cu simbolul '{symbol}' -> NU EXISTĂ TRANZIȚIE")
            return False
        
        next_state = transitions[transition_key]
        print(f"Pas {i+1}: Din starea '{current_state}' cu simbolul '{symbol}' -> starea '{next_state}'")
        current_state = next_state
    
    is_accepted = current_state in accept_states
    print(f"\nStare finală: {current_state}")
    print(f"Stări de acceptare: {accept_states}")
    print(f"String acceptat: {'DA' if is_accepted else 'NU'}")
    
    return is_accepted

def main():
    config = load_dfa_config('dfa_config.json')
    
    states = config['states']
    alphabet = config['alphabet']
    transitions = config['transitions']
    start_state = config['start_state']
    accept_states = config['accept_states']
    
    print("=== CONFIGURAȚIA DFA ===")
    print(f"Stări: {states}")
    print(f"Alfabet: {alphabet}")
    print(f"Stare inițială: {start_state}")
    print(f"Stări de acceptare: {accept_states}")
    print(f"Tranziții: {transitions}")
    print("\n" + "="*50 + "\n")

    test_strings = ["", "a", "ab", "aba", "abab", "baba", "aabb"]
    
    for test_string in test_strings:
        print(f"\n{'='*20} TEST {'='*20}")
        result = simulate_dfa(states, alphabet, transitions, start_state, accept_states, test_string)
        print(f"Rezultat: {'ACCEPTAT' if result else 'RESPINS'}")
        print("="*50)

    print("\n=== MOD INTERACTIV ===")
    while True:
        user_input = input("\nIntroduceți un string pentru testare (sau 'quit' pentru ieșire): ")
        if user_input.lower() == 'quit':
            break
        
        print(f"\n{'='*20} TEST INTERACTIV {'='*20}")
        result = simulate_dfa(states, alphabet, transitions, start_state, accept_states, user_input)
        print(f"Rezultat: {'ACCEPTAT' if result else 'RESPINS'}")
        print("="*50)

if __name__ == "__main__":
    main()