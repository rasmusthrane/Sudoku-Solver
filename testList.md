## Game    
[Ok] Given an initialized game, the dimensions should be 3x3 and 1 subgrid
[Ok] Given an initialzed game, no clues should be present
[Ok] Given an initialized game, all cells should be named correctly
[Ok] Given an initialized game, when injecting the clue '1' in A1 and '9' in C3 all other values should be empty
[Ok] Given a game with duplicate clues ('3' used twice), an error should be raised
[Ok] Given a game with invalid characters for clues (',' used), an error should be raised
[Ok] Given a game with too many clues (10 clues given), an error should be raised
[Ok] Given a game with too few clues (8 clues given), an error should be raised
[] Given a game where A1 is 1, all other cells should have values (2,...9) as candidates