import json

def load_tm_config(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Eroare: Fișierul {config_file} nu a fost găsit!")
        return None
    except json.JSONDecodeError:
        print(f"Eroare: Fișierul {config_file} nu este un JSON valid!")
        return None

def initialize_tape(input_string, blank_symbol):
    if not input_string:
        return [blank_symbol]
    return list(input_string)

def extend_tape_if_needed(tape, head_position, blank_symbol):
    while head_position >= len(tape):
        tape.append(blank_symbol)

    if head_position < 0:
        num_elements = abs(head_position)
        for _ in range(num_elements):
            tape.insert(0, blank_symbol)
        head_position = 0
    
    return head_position

def print_tape_state(tape, head_position, current_state, step):
    print(f"\nPas {step}:")
    print(f"Stare curentă: {current_state}")
    print(f"Poziția capului: {head_position}")

    tape_str = ""
    for i, symbol in enumerate(tape):
        if i == head_position:
            tape_str += f"[{symbol}]"
        else:
            tape_str += f" {symbol} "
    
    print(f"Bandă: {tape_str}")
    if 0 <= head_position < len(tape):
        print(f"Simbol citit: '{tape[head_position]}'")

def simulate_turing_machine(config, input_string, max_steps=100, step_by_step=True):
    states = config['states']
    transitions = config['transitions']
    start_state = config['start_state']
    accept_states = config['accept_states']
    reject_states = config['reject_states']
    blank_symbol = config['blank_symbol']
    
    print(f"\n=== SIMULARE MAȘINĂ TURING ===")
    print(f"String de intrare: '{input_string}'")

    tape = initialize_tape(input_string, blank_symbol)
    head_position = 0
    current_state = start_state
    step = 0
    
    if step_by_step:
        print_tape_state(tape, head_position, current_state, step)
    
    while step < max_steps:
        if current_state in accept_states:
            if step_by_step:
                print(f"\n ACCEPTAT! Am ajuns în starea de acceptare: {current_state}")
            return "ACCEPTED"
        
        if current_state in reject_states:
            if step_by_step:
                print(f"\nRESPINS! Am ajuns în starea de respingere: {current_state}")
            return "REJECTED"
        
        head_position = extend_tape_if_needed(tape, head_position, blank_symbol)
        current_symbol = tape[head_position]

        transition_key = f"{current_state},{current_symbol}"
        if transition_key not in transitions:
            if step_by_step:
                print(f"\nNU EXISTĂ TRANZIȚIE din starea '{current_state}' cu simbolul '{current_symbol}'")
                print("Mașina se oprește - RESPINS!")
            return "REJECTED"
        
        transition = transitions[transition_key]
        next_state = transition["next_state"]
        write_symbol = transition["write_symbol"]
        move_direction = transition["move_direction"]
        
        if step_by_step:
            print(f"\nTranziție: ({current_state}, '{current_symbol}') -> ({next_state}, '{write_symbol}', {move_direction})")

        tape[head_position] = write_symbol

        if move_direction == "R":
            head_position += 1
        elif move_direction == "L":
            head_position -= 1

        current_state = next_state
        step += 1
        
        if step_by_step:
            print_tape_state(tape, head_position, current_state, step)
            response = input("Apăsați Enter pentru următorul pas (sau 'q' pentru a ieși): ")
            if response.lower() == 'q':
                return "STOPPED"
    
    if step_by_step:
        print(f"\nTIMEOUT! Mașina a rulat {max_steps} pași fără să se oprească.")
    return "TIMEOUT"

def run_quick_tests(config):
    print("=== TESTARE RAPIDĂ ===")
    test_strings = ["", "01", "0011", "000111", "10", "001", "0101"]
    
    for test_string in test_strings:
        result = simulate_turing_machine(config, test_string, max_steps=100, step_by_step=False)
        print(f"String: '{test_string}' -> {result}")

def main():
    config = load_tm_config('turing_config.json')
    if config is None:
        return
    
    print("=== CONFIGURAȚIA MAȘINII TURING ===")
    print(f"Stări: {config['states']}")
    print(f"Alfabetul benzii: {config['tape_alphabet']}")
    print(f"Stare inițială: {config['start_state']}")
    print(f"Stări de acceptare: {config['accept_states']}")
    print(f"Stări de respingere: {config['reject_states']}")
    print(f"Simbolul gol: '{config['blank_symbol']}'")
    print(f"Numărul de tranziții: {len(config['transitions'])}")
    print("\n" + "="*60 + "\n")

    run_quick_tests(config)
    print("\n" + "="*60 + "\n")

    while True:
        print("\n=== MOD INTERACTIV ===")
        print("1. Simulare pas cu pas")  """Ma ajuta sa inteleg pas cu pas cum functioneaza"""
        print("2. Simulare rapidă")
        print("3. Afișare tranziții")
        print("4. Ieșire")
        
        choice = input("\nAlegeți opțiunea (1/2/3/4): ").strip()
        
        if choice == "4":
            print("La revedere!")
            break
        
        elif choice == "1":
            user_input = input("Introduceți string-ul de intrare: ").strip()
            result = simulate_turing_machine(config, user_input, max_steps=100, step_by_step=True)
            print(f"\nREZULTAT FINAL: {result}")
        
        elif choice == "2":
            user_input = input("Introduceți string-ul de intrare: ").strip()
            result = simulate_turing_machine(config, user_input, max_steps=100, step_by_step=False)
            print(f"\n REZULTAT FINAL: {result}")
        
        elif choice == "3":
            print("\n=== TRANZIȚII DISPONIBILE ===")
            for key, value in config['transitions'].items():
                state, symbol = key.split(',', 1)
                print(f"({state}, '{symbol}') -> ({value['next_state']}, '{value['write_symbol']}', {value['move_direction']})")
        
        else:
            print("Opțiune invalidă! Alegeți 1, 2, 3 sau 4.")

if __name__ == "__main__":
    main()