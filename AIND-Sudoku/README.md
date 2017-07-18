# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Naked Twins strategy uses elimination to remove possible solutions from a unit. Two boxes in a unit that have two values in common are said to be naked twins. This means that _none of their peer boxes can have these two values_, and hence these common two values must be eliminated from their peers. 

The implementation is two fold:
a) first, collect all naked twins
b) then, iterating over each naked twin, for every peer of the twin, eliminate the values of the twin from the peer. 

The implementation is shown here:
```
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

```

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:  
In a **Diagonal Sudoku**, the unique numbers constraint is also applied to the two big diagonals in the 9x9 square. 
The easisest way to implement diagonal sudoku is to add the diagonal units to the `unitlist` (which already contains column-wise, row-wise, and square-wise units).

Then run the regular `only_choice` and `eliminate` algorithms as usual.

The implementation is here:

```
DIAGONAL_SUDOKU = 1   # Flag=1 for Diagonal sudoku, else 0

diag1_units = [[rows[i] + cols[i] for i in range(len(rows))]]
diag2_units = [[rows[i] + cols_reverse[i] for i in range(len(rows))]]

# Create the Units, and Peers
if DIAGONAL_SUDOKU == 1:
    unitlist = row_units + column_units + square_units + diag1_units + diag2_units
else:
    unitlist = row_units + column_units + square_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

...
eliminate()   # as usual (per lessons)
...
only_choice()  # as usual (per lessons)

```

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

