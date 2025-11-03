## Sudoku 3x3 Alpha Test Cases

### 1. Initialization
- Given an empty game:
    - [Ok] The dimensions should be **3x3** with **1 subgrid**
    - [Ok] **No clues** should be present
    - [Ok] **All cells** should be named correctly
    - [Ok] There should only be one unit

### 2. Clue Injection
- When injecting clues:
    - [Ok] Injecting `'1'` in `A1` and `'9'` in `C3` &rarr; all other cells should be **empty**
    - [Ok] Injecting duplicate clues (e.g. `'3'` twice) &rarr; an **error** should be raised since duplicate clues cannot be injected
    - [Ok] Injecting invalid characters as clues (e.g. `','`) &rarr; an **error** should be raised
    - [Ok] Injecting too many characters as clues (e.g. 10) &rarr; an **error** should be raised
    - [Ok] Injecting too few characters as clues (e.g. 8) &rarr; an **error** should be raised

### 3. Cell Operations
- Given a game with clues:
  - [Ok] Updating the value of a **clue cell** &rarr; return `CANNOT_OVERWRITE_CLUE`
  - [Ok] Updating a cell with an **invalid character** &rarr; return `NOT_A_NUMBER`
  - [Ok] Updating the value of a **free cell** with a valid digit &rarr; return `OK` 
  - [Ok] Updating the value of a **free cell** with a valid digit &rarr; cell value should be **updated**
  - [Ok] Updating a **non-existent cell** &rarr; return `CELL_DOES_NOT_EXIST`
  - [Ok] Removing a value from a **non-existent cell** &rarr; return `CELL_DOES_NOT_EXIST`

### 4. Game State Evaluation
- [Ok] Given an **empty game** &rarr; state `'ongoing'`
- [Ok] When a **constraint violation** occurs (e.g., same digit twice) &rarr; state `'constraint_violation'`
- [Ok] When a **violation is fixed** by removing a violating digit &rarr; state `'ongoing'`
- [Ok] When **all digits** are placed with **no violations** &rarr; state `'won'`

### 5. Candidates Management
- Given an empty game:
  - [Ok] Place `1` in `A1` and `2` in `C3` &rarr; all other cells have **candidates 3–9**. Remove `2` from `C3` &rarr; all other cells have **candidates 2–9**

## Sudoku 4x4 Beta Test Cases
### 1. Initialization
- Given an empty game:
    - [Ok] The dimensions should be **4x4** with **4 subgrids**
    - [Ok] There should exist 12 units
    - [Ok] The units that `A1` belongs to should be `A1,A2,B1,B2`, `A1,A2,A3,A4` and `A1,B1,C1,D1`             
    - [Ok] **No clues** should be present
    - [Ok] **All cells** should be named correctly

### Cell Operations
- Given a game
  - [Ok]  Place `9` in `A1` -> return `INVALID_DIGIT`

### Game State Evaluation  
- [Ok] Given a game with `1234` in row `A` and `3412` in row `B` -> state `'ongoing'`
  - [Ok] Ask what cells violate constraint -> return an empty list
- [Ok] Given a game with `1234` in row `A` and `2341` in row `B` -> state `'constraint_violation'` 
  - [Ok] Ask what cells violate constraint -> return `A2` `B1`, `A4` and `B3` 
- [Ok] Given a game with `1234` in row `A` and `3412` in row `B` and `4321` in row `C` and `2143` in row `D` -> state: `'won'`   
  - [Ok] Ask what cells violate constraint -> return an empty list
- [Ok] Given a game with `1234` in row `A` and `3412` in row `B` and `4321` in row `C` and `2234` in row `D` -> state: `'constraint_violation'`   
  - [Ok] Ask what cells violate constraint -> return `A2`, `A3`, `A4`, `D1`, `D2`, `D3`, `D4` 

### Candidates Management
- Given an empty game:
  - [Ok] Place `1` in `A1`, `2` in `A2`, `3` in `B2`-> `B1` should have candidate `4`, `A3` and `A4` should have candidates `34`, `B3` and `B4` should have candidates `234`, `D4` should have candidates `1234`
  - [Ok] Place `1` in `A1`, `2` in `A4` and `3` in `D4` and then remove the value in `A4` -> `A4` should have candidates `24`

### GUI
- Given an empty game, an app and a test client
  - [Ok] the status should be OK when the client tries to place digit `1` in `A1`, and the change in value should propagate to game
  - [Ok] the status should be CANNOT_OVERWRITE_CLUE when the client tries to place overwrite a clue, and the attempted change in value should not happen


## Sudoku 9x9 Gamma Test Cases
### Initialization
- Given an empty game:
    - [Ok] The dimensions should be **9x9** with **9 subgrids**
    - [Ok] There should exist 9+9+9=27 units
    - [Ok] The units that `A1` belongs to should be `A1,A2,A3,A5,A6,A7,A8,A9`, `A1,B1,C1,D1,E1,F1,G1,H1,I1` and `A1,A2,A3,B1,B2,B3,C1,C2,C3`
    - [Ok] **No clues** should be present

### Clue Injection
- When injecting clues:
    - [Ok] Injecting invalid characters as clues (e.g. `'!'`) &rarr; an **error** should be raised
    - [Ok] Injecting too many characters as clues (e.g. 82) &rarr; an **error** should be raised
    - [Ok] Injecting too few characters as clues (e.g. 80) &rarr; an **error** should be raised
    - [] Injecting clues that violate a constrant &rarr; an **error** should be raised

### Cell Operations
- Given a game
  - [Ok]  Place `9` in `A1` -> return `OK`
  - [Ok]  Place `11` in `I9` -> return `INVALID_DIGIT`
  - [OK] Place `!!` in `B3` -> return `NOT_A_NUMBER` 

### Game State Evaluation  
- [Ok] Given a game with `123...789` in row `A` and `247.5..9.` in row `H` -> state `'ongoing'`
- [Ok] Given a game with `123...789` in row `A` and `247.5.98.` in row `H` -> state `'constraint_violation'` 
- [Ok] Given a game with filled with valid and complete rows -> state `'won'`

### Candidates Management
- Given a game where the clue `3` is placed in `A6`:
  - [Ok] Place `1` in `A1`, `2` in `B4`, `9` in `C6`-> `A2` should have candidates `2456789`,  `B5` should have candidates `1245678` and `D9` should have candidates `123456789

### Solver
- [Ok] Given an easy Sudoku solver should find the solution
- Given an intermediate sudoku