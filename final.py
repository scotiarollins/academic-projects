#
# starter code for LifeBoard, based on the C4 Board class!
#

from random import choice
from time import sleep

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit

class LifeBoard:
    """ a foundation for a Game-of-Life LifeBoard class, 
        similar to and based on the Connect Four Board class
    """

    def __init__(self,width=20,height=20):
        """ constructor, very similar to C4 Board's constructor """
        self.width = width
        self.height = height
        #
        # start with all 0's
        #
        self.data = [ [0 for c in range(self.width)] for r in range(self.height) ]
        self.walker = Walker(0,0, self)     # the walker's initial position

    def __repr__(self):
        """ returns a string version of the current LifeBoard object """
        W = self.width
        H = self.height
        D = self.data

        s = ""  # the string, to be accumulated here
        walker_icon = "👻"
        s += "\n"  # start with a blank line
        for r in range(H):
            for c in range(W):
                if r == self.walker.row and c == self.walker.col:
                    s+= walker_icon #f"{walker_icon} "
                else:
                    s += f"{D[r][c]} "
            s += "\n"   # add a newline at the end of each row

        return s
    
    def printBoard(self, A):
        """This function prints the 2D list-of-lists A.
        """
        for row in A:                # row is the whole row
            print()
            for col in row:          # col is the individual element
                print(col, end = '') # Print that element
    
    def countNeighbors(self, row, col, A):
        """
        Counts neighbors around cell at row, col
        """

        num = 0

        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if A[r][c] == 1:
                    num += 1
        
        if A[row][col] == 1:
            num -= 1

        return num
    
    def createOneRow(self, width):
        """Returns one row of zeros of width "width"...  
       You might use this in your createBoard(width, height) function.
       """
        row = []
        for col in range(width):
            row += [0]
        return row


    def createBoard(self, width, height):
        """Returns a 2D array with "height" rows and "width" columns.
        """
        A = []
        for row in range(height):
            A += [self.createOneRow(width)]  # Use the above function so that SOMETHING is one row!

        
        
        return A
    
        
    def copy(self):
        """Returns a DEEP copy of the 2D board."""

        height = self.height
        width = self.width
        new_board = self.createBoard(width, height)

        for row in range(1, height - 1):
            for col in range(1, width - 1):
                new_board[row][col] =  self.data[row][col]# What should be here, in order to
                # ..copy each element of A into the corresponding spot in newA?

        newLB = LifeBoard(width,height)
        newLB.data = new_board
        return newLB

    def next_air_generation(self):
        """ re-randomize the inner cells """
        W = self.width
        H = self.height
        D = self.data

        for r in range(1,H-1):      # don't touch the edges
                D[r][2] = 1 
        
    
    def next_random_generation(self):
        """ re-randomize the inner cells """
        W = self.width
        H = self.height
        D = self.data

        for r in range(1,H-1):      # don't touch the edges
            for c in range(1,W-1):  # don't touch the edges
                D[r][c] = choice( [0,1] )

    def next_life_generation(self):
        """Makes a copy of the board and then advances one
        generation of Conway's Game of Life within
        the *inner cells* of that copy.
        The outer edge always stays at 0.
        """

        height = self.height
        width = self.width
        newLB = self.copy()
        new_board = newLB.data

        #print(self.countNeighbors(2,1,new_board))

        for r in range(0, height-1):
            for c in range( 0, width-1):
                n = self.countNeighbors(r, c, self.data)
                if n < 2:                   #Rule: Cell dies if less than 2 neighbors
                    new_board[r][c] = 0
                    #print('1')
                if n > 4:                 #Rule: Cell dies if more than 4 neighbors
                    new_board[r][c] = 0
                    #print('2')
                elif n == 3 or n == 6:                #Rule: Cell is born if has 3 or 6 neighbors  (High Life)
                    new_board[r][c] = 1
                    #print('3')

                else:                       
                    new_board[r][c] = new_board[r][c]
     
    
        
        self.data = new_board

    def interact(self):
        """Kills live cells at the walker's position. 
        """

        if self.board.data[self.row][self.col] == 1:
            self.board.data[self.row][self.col] = 0         # Kill the cell

    
    def move(self):
        """
        Moves the walker randomly within board boundaries.

        """

        from random import choice

        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        dr, dc = choice(directions)
        new_row = self.row + dr
        new_col = self.col + dc

        if 0 <= new_row < self.board.height and 0 <= new_col < self.board.width:
            self.row = new_row
            self.col = new_col
            


    def next_life_generation_with_walker(self):
        """

        Advance the board while including the walker
  
        """

        self.next_life_generation()
        self.walker.move()
        self.walker.interact()

    def count_live_cells(self):

        """
        Counts the number of live cells at the present generation
        """

        num = 0


        for col in range(self.width):
            for row in range(self.height):
                if self.data[row][col] == 1:
                    num += 1

        return num


    def run_generations(self,num_gens):
        """ runs num_gens number of generations 
            printing as we go...
        """
        print(self)

        live_cells_list = []

        for gen in range(num_gens):
            print("Generation #", gen)
            self.next_life_generation_with_walker()     # new generation (this is a _naive_ approach!)
            print(self)
            live_cells_list.append(self.count_live_cells())
            sleep(0.05)

        print("Done!")
        print('There are '+ str(self.count_live_cells())+ ' live cells on the board.')

        return live_cells_list


class Walker:
    def __init__(self, start_row, start_col, board):
        self.row = start_row
        self.col = start_col
        self.board = board

    def move(self):
        """Move the walker. You can customize its movement logic here."""
        self.row = (self.row + 1) % self.board.height  # Example: move down
        self.col = (self.col + 1) % self.board.width   # Example: move right

    def interact(self):
        """Kill any live cell the walker touches."""
        if self.board.data[self.row][self.col] == 1:
            self.board.data[self.row][self.col] = 0


## SETUP ##

#Choosing the board size
LB = LifeBoard(20,20)   
LB.next_air_generation()

data = LB.run_generations(200)
df = pd.DataFrame(data, columns = ["Numbers"])

##Making an excel spreadsheet with numbers as columns:
#df.to_excel("numbers.xlsx", index = False)

#CREATE A PLOT
plt.plot(data, label = "Live Cells")
plt.xlabel('Generation')
plt.ylabel('Number of Live Cells')
plt.title('Live Cells Across Generations') #Plot title


## EXPONENTIAL CURVE
# def exponential(x, A, B):
#     return A * np.exp(B * x)
#params, covariance = curve_fit(exponential, x, y, p0 = [y[0], 0.01])
#A, B = params
#fitted_curve = exponential(x, A, B)
#plt.plot(x, fitted_curve, label = 'Exponential Fit', color = 'red', linestyle='--')


#QUADRATIC LINE OF BEST FIT
x = np.arange(len(data))
y = np.array(data)

coefficients = np.polyfit(x,y, 2)
best_fit_curve = np.polyval(coefficients,x)

plt.legend()
plt.plot(x, best_fit_curve, label = 'Best Fit Curve')
plt.show()