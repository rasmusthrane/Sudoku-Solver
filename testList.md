## Game    
[Ok] Given an initialized game, the dimensions should be 3x3 and 1 subgrid
[Ok] Given an initialzed game, no clues should be present
[Ok] Given an initialized game, all cells should be named correctly
[Ok] Given an initialized game, when injecting the clue '1' in A1 and '9' in C3 all other values should be empty
[Ok] Given a game with duplicate clues ('3' used twice), an error should be raised
[Ok] Given a game with invalid characters for clues (',' used), an error should be raised
[Ok] Given a game with too many clues (10 clues given), an error should be raised
[Ok] Given a game with too few clues (8 clues given), an error should be raised
[Ok] Given a game with clues, if trying to replace the value of the cell holding the clue, the status CANNOT_OVERWRITE_CLUE should be returned
[Ok] Given a game with clues, if trying to replace the value of a free cell, the status OK should be returned
[Ok] Given a game with clues, when updating a cell value, the value of the cell should be updated
[Ok] Given a game with clues, when updating a cell value with an invalid character, the status INVALID_CHAR should be returned
[Ok] Given a game, when updating a cell that does not exist, the status CELL_DOES_NOT_EXIST should be returned
[Ok] Given an empty game, the game state 'ongoing' should be returned
[Ok] Given a game, if the player puts down the same digit in two different cells and checks game state, the string 'constrain_violation' is returned
[Ok] Given a game, if the player violates a constrain and then fix the violation by removing the digit, the game state 'ongoing' should be returned
[] Given a game, if 1 is placed in A1 and 2 is placed in C3 then all other cells should have 3:9 as candidates. If 2 is removed from C3 then all other cells should have 2:9 as candidates
[Ok] Given a game, if all digits are placed initially and no constraints are violated, the game state should we 'win'


[] Given a game where A1 is 1, all other cells should have values (2,...9) as candidates