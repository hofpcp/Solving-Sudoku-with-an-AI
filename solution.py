

assignments = [] # empty list for populating in assign_values function

# helper function for crossing lists 
def cross(A, B):
    return [s+t for s in A for t in B]

# create all variables for sudoku board, incl. boxes, columns, rows, squares, diagonals and peers 
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [['A1','B2','C3','D4','E5','F6','G7','H8','I9'],['A9','B8','C7','D6','E5','F4','G3','H2','I1']] 
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


# Assigns a value to a given box and updates the board, needed for visualization
def assign_value(values, box, value):
    
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    
    
    return values

# Eliminates "Naked Twins", i.e. find 2 digit boxes within same unit (col, row, square, diag) that are equal
# and removes these digits within all other boxes within same unit
def naked_twins(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 2]
    for box in solved_values:
        digits = values[box]
        for peer in peers[box]:
            if values[peer] == digits:
                gen = (x for x in set(peers[box]).intersection(peers[peer]) if x not in (box, peer))
                for x in gen:
                    for i in digits:
                        #values[x] = values[x].replace(i,'')
                        assign_value(values, x, values[x].replace(i,''))
                        
                
    return values

# converts a grid in string form, to a 2d Sudoku board in dictionary form, replaces all empty boxes with digits
# '123456789'
def grid_values(grid):
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    grid = dict(zip(boxes,chars))
    for key, value in grid.items():
        grid = assign_value(grid, key, value)
    
    
        
    return grid
        
# displays the Sudoku dictionary in grid form
def display(values):
    
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
        for c in cols))
        if r in 'CF': print(line)
        
    return

# finds all already solved values, i.e. boxes with only 1 value and removes same from all peers
# in row, col, square, diag
def eliminate(values):

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values, peer, values[peer].replace(digit,''))    
        
    return values

# searches all units and where any specific box has a unique digit compared to rest in unit, update with this 
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
        
    return values

# iterate thorugh functions 'eliminate', 'naked twins', 'only choice', until Sudoku is either solved or stalled
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    
    return values


# Search function starts by calling 'reduce_puzzle' and gets either solved or
# stalled puzzle back. If stalled finds a box with lowest amount of unsolved digits, chooses 1st digit in this
# and attempts solving with reduce puzzle. Iterates over this 'Search" method until solved. 
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# call function with string representing Sudoku grid and get solved Sudoku grid back.       
def solve(grid):
    
    soduko_grid = grid_values(grid)
    
  
    return search(soduko_grid)

    

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
