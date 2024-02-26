# Discord Spellcast Solver

## This Python command-line program solves for the biggest possible word in Discord's "Spellcast" game.

To run, install python3, and run solver_v2.py.

## Use Instructions

Within the command-line, enter in each letter, from left to right, top to bottom.
- If the letter is a Double(DL), place a number 1 in front of the character.
- If the letter is a Triple(TL) place a 3 in front of the character.
- If the letter has a flag for 2x word, place a 2 in front of the character.

An example input would be: 
ox2viodtgfhryrhd1gizge3utare

After pressing enter, the program will then calculate every possible word that can be made from the current board, based on the dictionary provided in dictionary.txt

## Planned Features
- Allow for calculating the best words if power-ups are used. Power-ups within the game allow for players to substitute a character on the board for any letter, or shuffle the entire board.
- Implement a GUI
- Implement the game's jewels into the solver, which can be spent to use powerups, or are added to the player's score at the end of the game if unused.

## Bugs
- The game's actual dictionary is not known, so a dictionary was found on the internet that was found to be somewhat accurate. However, some words may be missing, and some invalid words may be provided by the program.
  
