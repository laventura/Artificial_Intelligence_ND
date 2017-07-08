assignments = []

###
ALL_DIGITS = '123456789'
rows = 'ABCDEFGHI'
cols = ALL_DIGITS
cols_reverse = cols[::-1]   # reversed digits

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

###################### NAKED TWINS ##########################################
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    naked_twins = []
    for box in values:
        if len(values[box]) == 2:
            for peer in peers[box]:
                # collect all naked twins
                if box < peer and values[peer] == values[box]:
                    naked_twins.append([box, peer])
    
    for twin in naked_twins:
        # get all units that contain these twins
        units_with_twins = [u for u in unitlist if twin[0] in u and twin[1] in u]
        for unit in units_with_twins:
            for box in unit:
                if box != twin[0] and box != twin[1]:
                    # eliminate these naked twins as possibilities for their peers
                    values[box] = values[box].replace(values[twin[0]][0], '')
                    # visualize it
                    assign_value(values, box, values[box])
                    
                    values[box] = values[box].replace(values[twin[0]][1], '')
                    assign_value(values, box, values[box])
    
    if len([box for box in values.keys() if len(values[box]) == 0]):
        return False
    
    return values



#################### DIAGONAL SUDOKU #######################################
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

# -- Note - following code from lessons --
# Create Boxes (9x9)
boxes = cross(rows, cols)


## Now get the Row Units, Column Units and Square Units
# One UNIT == a set of 9 Boxes (row, column or a 9x9 box)

row_units = [cross(r, cols) for r in rows]
# rows_units[0] = ['A1', 'A2', ...'A9'] --> top most row

column_units = [cross(rows, c) for c in cols]
# column_units[0] = ['A1', 'B1', ... 'I1'] --> first column

square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']

# !!!!!!!!!!!!!!!!!!!!!! NOTE: for Diagonal Sudoku, set this to 1; otherwise set it to 0
DIAGONAL_SUDOKU = 1

diag1_units = [[rows[i] + cols[i] for i in range(len(rows))]]
diag2_units = [[rows[i] + cols_reverse[i] for i in range(len(rows))]]

# Create the Units, and Peers
if DIAGONAL_SUDOKU == 1:
    unitlist = row_units + column_units + square_units + diag1_units + diag2_units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid, show_dot=False):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
        show_dot - Show '.' if True, else show all values ('123456789')
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    for c in grid:
        if c == '.':  # i.e. blank value
            if show_dot:
                values.append('.')
            else:
                values.append(ALL_DIGITS)
        elif c in ALL_DIGITS:
            values.append(c)
    
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print('\n')
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    return_values = values.copy()
    solved_values = [box for box in return_values.keys() if len(return_values[box]) == 1]

    for box in solved_values:
        digit = return_values[box]
        for peer in peers[box]:
            return_values[peer] = return_values[peer].replace(digit, '')
            # visualize
            assign_value(return_values, peer, return_values[peer])
    
    return return_values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: value: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    return_values = values.copy()
    for unit in unitlist:
        for digit in ALL_DIGITS:
            dplaces = [box for box in unit if digit in return_values[box]]

            if len(dplaces) == 1:
                return_values[dplaces[0]] = digit
                # for visualization
                assign_value(return_values, dplaces[0], digit)

    return return_values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    
    Input: A sudoku in dictionary form.
    
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # 1 - Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # 2 - Use the Eliminate Strategy
        values = eliminate(values)

        # 3 - Use the Only Choice Strategy
        values = only_choice(values)

        # 4 - Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # 5 - If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # 6 - Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """ Using depth-first search and propagation, create a search tree and solve the sudoku.
        Tries all possible values for a given box (using sub-trees)
        At any sub-tree, choose a box with the fewest possible values
    """
    # 1 - reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False    ## Fail early
    
    if all(len(values[b]) == 1 for b in boxes):
        return values   ## SOLVED!

    # 2 - Choose one of the unfilled squares with the fewest possibilities
    n,b = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)

    # 3 - Now use recursion to solve each one of the resulting sudokus, and if one returns a value
    for value in values[b]:
        new_sudoku = values.copy()
        new_sudoku[b] = value 

        # 3.1 - try search on a sub-tree
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # 0 - Show the Before puzzle
    before_puzzle = grid_values(grid, show_dot=True)
    print('BEFORE')
    display(before_puzzle)
    
    # 1 - Convert to grid
    grid = grid_values(grid)
    
    # 2 - search (recursive) within the grid
    possibly_solved = search(grid)
    
    # 3 - show results
    print('\nAFTER')
    #display(possibly_solved)

    return possibly_solved

if __name__ == '__main__':

    if DIAGONAL_SUDOKU == 1:
        print('** Attempting Diagonal Sudoku **')
    else:
        print('-- Attempting normal (non-diagonal) Sudoku --')

    diag_sudoku1 = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku2 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    diag_sudoku3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    for sudoku in [diag_sudoku1, diag_sudoku2, diag_sudoku3]:
        print('------------------------------- Solving one Sudoku ---------------------- ')
        maybe_solved = solve(sudoku)
        if not maybe_solved:
            print('  !! Sudoku not solved (consider setting DIAGONAL_SUDOKU=0 in code)')
        else:
            display(maybe_solved)
    #display(solve(diag_sudoku_grid))

    #print('**** Running second test ****')
    #diag_sudoku2 = '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
    #display(solve(diag_sudoku2))

    #print('**** Running third test ****')
    #diag_sudoku3 = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    #display(solve(diag_sudoku3))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
