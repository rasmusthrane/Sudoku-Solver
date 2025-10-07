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
  - [Ok] Updating a cell with an **invalid character** &rarr; return `INVALID_CHAR`
  - [Ok] Updating the value of a **free cell** with a valid digit &rarr; return `OK` 
  - [Ok] Updating the value of a **free cell** with a valid digit &rarr; cell value should be **updated**
  - [Ok] Updating a **non-existent cell** &rarr; return `CELL_DOES_NOT_EXIST`
  - [Ok] Removing a value from a **non-existent cell** &rarr; return `CELL_DOES_NOT_EXIST`

### 4. Game State Evaluation
- [Ok] Given an **empty game** &rarr; state `'ongoing'`
- [Ok] When a **constraint violation** occurs (e.g., same digit twice) &rarr; state `'constrain_violation'`
- [Ok] When a **violation is fixed** by removing a violating digit &rarr; state `'ongoing'`
- [Ok] When **all digits** are placed with **no violations** &rarr; state `'win'`

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

### Candidates Management
- Given an empty game:
  - [Ok] Place `1` in `A1`, `2` in `A2`, `3` in `B2`-> `B1` should have candidate `4`, `A3` and `A4` should have candidates `34`, `B3` and `B4` should have candidates `234`, `D4` should have candidates `1234`
  - [Ok] Place `1` in `A1`, `2` in `A4` and `3` in `D4` and then remove the value in `A4` -> `A4` should have candidates `24`