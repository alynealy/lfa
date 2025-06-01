import json
from collections import deque

def load_config(config_file):
    """Load and validate PDA configuration"""
    with open(config_file) as f:
        config = json.load(f)
  
    required_fields = ['states', 'input_alphabet', 'stack_alphabet', 
                      'start_state', 'initial_stack_symbol', 'accept_states', 
                      'transitions']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")

    config['states'] = set(config['states'])
    config['input_alphabet'] = set(config['input_alphabet'])
    config['stack_alphabet'] = set(config['stack_alphabet'])
    config['accept_states'] = set(config['accept_states'])
    
    transitions = {}
    for t in config['transitions']:
        key = (t['current_state'], t['input'], t['pop'])
        val = (t['next_state'], t['push'])

        if t['current_state'] not in config['states']:
            raise ValueError(f"Invalid current state: {t['current_state']}")
        if t['input'] != 'epsilon' and t['input'] not in config['input_alphabet']:
            raise ValueError(f"Invalid input symbol: {t['input']}")
        if t['pop'] not in config['stack_alphabet']:
            raise ValueError(f"Invalid pop symbol: {t['pop']}")
        if t['next_state'] not in config['states']:
            raise ValueError(f"Invalid next state: {t['next_state']}")
        for sym in t['push']:
            if sym not in config['stack_alphabet']:
                raise ValueError(f"Invalid push symbol: {sym}")

        if key not in transitions:
            transitions[key] = []
        transitions[key].append(val)
    
    config['transitions'] = transitions
    return config

def process_input(pda, input_str):
    """Simulate PDA execution with detailed output"""
    # Validate input characters
    for char in input_str:
        if char not in pda['input_alphabet']:
            print(f"Invalid input character: '{char}'")
            return False

    stack = [pda['initial_stack_symbol']]
    queue = deque([(pda['start_state'], list(input_str), stack, [])])
    visited = set()
    
    print(f"\nProcessing: '{input_str}'")
    print("=" * 40)
    
    while queue:
        current_state, remaining_input, stack, path = queue.popleft()
        
        print(f"State: {current_state}")
        print(f"Remaining: '{''.join(remaining_input)}'")
        print(f"Stack: {''.join(stack[::-1]) if stack else 'ε'}")
        if path:
            print("Path:")
            for step in path:
                print(f"  {step}")
        print("-" * 40)
        
        if not remaining_input and current_state in pda['accept_states']:
            print("\nACCEPTED")
            return True
 
        config_id = (current_state, tuple(remaining_input), tuple(stack))
        if config_id in visited:
            continue
        visited.add(config_id)
        
        input_symbol = remaining_input[0] if remaining_input else 'epsilon'
        pop_symbol = stack[-1] if stack else None
        
        _process_transition(pda, queue, current_state, input_symbol, pop_symbol,
                               remaining_input, stack, path)

        _process_transition(pda, queue, current_state, 'epsilon', pop_symbol,
                               remaining_input, stack, path)
    
    print("\nREJECTED")
    return False

def _process_transition(pda, queue, current_state, input_sym, pop_sym,
                      remaining_input, stack, path):
    """Handle transitions and add new configurations to queue"""
    key = (current_state, input_sym, pop_sym)
    if key not in pda['transitions']:
        return

    remaining = remaining_input.copy()
    if input_sym != 'epsilon' and remaining:
        remaining.pop(0)

    for next_state, push_symbols in pda['transitions'][key]:
        new_stack = stack.copy()
        if new_stack:
            new_stack.pop()
        new_stack.extend(reversed(push_symbols))
        
        new_path = path + [
            f"{current_state} --{input_sym},{pop_sym}/{''.join(push_symbols)}--> {next_state}"
        ]
        queue.append((next_state, remaining, new_stack, new_path))

def main():
    """Interactive PDA tester"""
    try:
        pda = load_config('config.json')
    except Exception as e:
        print(f"Config error: {e}")
        return

    print("PDA Interactive Tester")
    while True:
        input_str = input("\nEnter input string (q to quit): ").strip()
        if input_str.lower() == 'q':
            break
        if not all(c in pda['input_alphabet'] for c in input_str):
            invalid = [c for c in input_str if c not in pda['input_alphabet']]
            print(f"Invalid characters: {invalid}")
            continue
            
        process_input(pda, input_str)

if __name__ == "__main__":
    main()
