## Game    
[Ok] Given an initialized game, the dimensions should be 3x3 and 1 subgrid
[Ok] Given an initialzed game, no clues should be present
[Ok] Given an initialized game, all cells should be named correctly
[Ok] Given an initialized game, when injecting the clue '1' in A1 and '9' in C3 all other values should be empty
[Ok] Given a game, when injecting an invalid set of clues ('3' used twice), Status.DUPLICATE_CLUE should be returned
[Ok] Given a game, when injecting an invalid character, Status.INVALID_CHAR should be returned
[Ok] Given a game, when injecting a too long string representation, Status.TOO_MANY_CHARS should be returned
[Ok] Given a game, when injecting a too short string representation, Status.TOO_FEW_CHARS should be returned