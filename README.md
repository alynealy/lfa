# LFA - Limbaje Formale și Automate

Simulatoare pentru automate finite, automate cu stivă și mașini Turing implementate în Python.

## Ce conține

- **DFA** (Deterministic Finite Automaton) - automat finit determinist
- **NFA** (Non-deterministic Finite Automaton) - automat finit non-determinist cu epsilon-tranziții
- **PDA** (Pushdown Automaton) - automat cu stivă
- **Turing Machine** - mașina Turing

## Cum rulezi

```bash
python dfa.py          # Pentru DFA
python nfa.py          # Pentru NFA  
python pda.py          # Pentru PDA
python turing.py       # Pentru Mașina Turing
```

## Fișiere

```
dfa.py + dfa_config.json        # Simulator DFA
nfa.py + nfa_config.json        # Simulator NFA
pda.py + pda.json               # Simulator PDA  
turing.py + turing_config.json  # Simulator Mașina Turing
```

## Configurare

Automatele se configurează prin fișiere JSON. Exemplu pentru DFA:

```json
{
  "states": ["q0", "q1", "q2"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0,a": "q1",
    "q0,b": "q0"
  },
  "start_state": "q0",
  "accept_states": ["q1"]
}
```

## Funcționalități

- **Mod interactiv** - introduce string-uri pentru testare
- **Vizualizare pas cu pas** - vezi cum funcționează automatul
- **Testare automată** - rulează teste predefinite
- **Validare input** - verifică alfabetul și tranziții

## Exemple implementate

- **DFA**: Recunoaște cuvinte cu număr impar de 'a'
- **NFA**: Pattern matching cu epsilon-tranziții
- **PDA**: Paranteze balansate
- **Turing**: Limbajul {0^n 1^n | n ≥ 0}

## Cerințe

Python 3.7+
