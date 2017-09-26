# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver
### Student: Peter Carsten Petersen

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked twins is the constraint scenario where 2 boxes within the same space (column, row, square, diagonal) share the same
2 digits as possible solution. This in turn means that no other box within the same space can use these digits in the 
solution, and we can therefore remove these as possible digits in all but the 2 "Naked Twins" boxes.



# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: In order to solve the diagonal Sudoku problem, we introduce the 2 diagonals (from A1-I9 and I1-A9), as new constraint
units as well as include in "Peers" for all boxes on the diagonal planes. This in turn ensures that when the puzzle is being
solved, via the various techniques (Eliminate, Only Choice, Naked Twins, etc.) it will also follow the constraint of fitting 
digits 1-9 on the diagonal planes, as well as in columns, rows and Square units.


