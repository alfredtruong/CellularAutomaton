# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:10:06 2020

https://medium.com/better-programming/how-to-write-conwells-game-of-life-in-python-c6eca19c4676

@author: ahkar
"""

from random import randint

DEBUG=0

class Cell():
    def __init__(self):
        self._status=False
        
    # set status of dead
    def set_dead(self):
        self._status=False

    # set status to alive
    def set_alive(self):
        self._status=True

    # is cell alive
    def is_alive(self):
        if self._status:
            return True
        else:
            return False

    # what board should print
    def get_print_character(self):
        if self.is_alive():
            return 'x'
        else:
            return '.'
        
    # print
    def __str__(self):
        return self.get_print_character()

'''
b=Board()
b.draw_board()
b._grid[0][0].is_alive()
b._grid[0][1].is_alive()
b._grid[0][0].get_print_character()
print(b._grid[0][0])
'''

class Board():
    # constructor
    def __init__(self,nrow=10,ncol=10):
        self._nrow=nrow
        self._ncol=ncol
        self._grid=[[Cell() for col_cells in range(self._ncol)] for row_cells in range(self._nrow)]
    
        self._generate_board()

    # draw board on terminal
    def draw_board(self):
        print('\n'*10)
        print('printing board')
        
        for row in self._grid:
            for col in row:
                print(col.get_print_character(),end='')
            print() # new line
            
    # initial random generation
    def _generate_board(self): 
        for row in self._grid:
            for col in row:
                # 33% chance of live spawn
                chance=randint(0,2)
                if chance == 1:
                    col.set_alive()

    # left index
    def get_left_index(self,col):
        return col-1 if col>0 else self._ncol-1
        
    # right index
    def get_right_index(self,col):
        return 0 if col==(self._ncol-1) else col+1
    
    # up index
    def get_up_index(self,row):
        return row-1 if row>0 else self._nrow-1
  
    # down index
    def get_down_index(self,row):
        return 0 if row==(self._nrow-1) else row+1
    
    # find neighbours
    def get_neighbours(self,row,col):
        neighbours=[]
        
        upindex=self.get_up_index(row)
        downindex=self.get_down_index(row)
        leftindex=self.get_left_index(col)
        rightindex=self.get_right_index(col)

        if DEBUG>0:
            print('%s\t%s\t%s\t%s\t'%(upindex,downindex,leftindex,rightindex))
    
            print([upindex,leftindex])       # above row
            print([upindex,col])             # above row
            print([upindex,rightindex])      # above row
            print([row,leftindex])           # current row
            print([row,rightindex])          # current row
            print([downindex,leftindex])     # below row
            print([downindex,col])           # below row
            print([downindex,rightindex])    # below row
    
            print(self._grid[upindex][leftindex].is_alive())       # above row
            print(self._grid[upindex][col].is_alive())             # above row
            print(self._grid[upindex][rightindex].is_alive())      # above row
            print(self._grid[row][leftindex].is_alive())           # current row
            print(self._grid[row][rightindex].is_alive())          # current row
            print(self._grid[downindex][leftindex].is_alive())     # below row
            print(self._grid[downindex][col].is_alive())           # below row
            print(self._grid[downindex][rightindex].is_alive())    # below row
        
        # populate neighbours
        neighbours.append(self._grid[upindex][leftindex])       # above row
        neighbours.append(self._grid[upindex][col])             # above row
        neighbours.append(self._grid[upindex][rightindex])      # above row
        neighbours.append(self._grid[row][leftindex])           # current row
        neighbours.append(self._grid[row][rightindex])          # current row
        neighbours.append(self._grid[downindex][leftindex])     # below row
        neighbours.append(self._grid[downindex][col])           # below row
        neighbours.append(self._grid[downindex][rightindex])    # below row

        # return
        return neighbours
                    
    # update generation for all cells
    def update_board(self):
        print('updating board')
        goes_alive=[]
        gets_killed=[]
        
        # count of all live guys
        live_population=0
        
        for row in range(self._nrow):
            for col in range(self._ncol):
                # increment population counter if alive
                if self._grid[row][col].is_alive():
                    live_population+=1
                    
                # check neighbour
                neighbours = self.get_neighbours(row,col)
                
                live_neighbours=0
                
                for neighbour in neighbours:
                    # check live status
                    if neighbour.is_alive():
                        live_neighbours+=1
                
                cell_obj=self._grid[row][col] 
                cell_status=cell_obj.is_alive()
                
                '''
                rules
                
                If a cell is alive it will:
                    Die if there are less than two living neighbours.
                    Continue living if there are exactly two or three living neighbours.
                    Die if there are more than three living neighbours.
                If a cell is dead it will:
                    Resurrect (become alive) if there are exactly three living neighbours.

                '''
                # find new status given conditions
                action='none'
                if cell_status:
                    if live_neighbours<2:
                        gets_killed.append(cell_obj)
                        action='gets_killed'
                    if live_neighbours>3:
                        gets_killed.append(cell_obj)
                        action='gets_killed'
                else:
                    if live_neighbours==3:
                        goes_alive.append(cell_obj)
                        action='goes_alive'
                        
                if DEBUG>0:
                        print('%s-%s\t:\tlive_neighbours\t%s\t%s' % (row,col,live_neighbours,action))


        # set updated cell statuses
        for cell in goes_alive:
            cell.set_alive()
            
        for cell in gets_killed:
            cell.set_dead()

        # is worth recomputing
        worth_continuing=True
        if len(goes_alive)==0 and len(gets_killed)==0:
            worth_continuing=False
            
        # state current population
        if worth_continuing and live_population > 0:
            return True
        else:
            return False

'''
b=Board()

b.get_down_index(0)
b.get_down_index(8)
b.get_down_index(9)

b.get_up_index(0)
b.get_up_index(1)
b.get_up_index(9)

b.get_right_index(0)
b.get_right_index(8)
b.get_right_index(9)

b.get_left_index(0)
b.get_left_index(1)
b.get_left_index(9)
'''
    
# putting it all together     
def main(user_rows,user_cols,autorun=False):
    '''
    # user settings
    user_rows=int(input('nrows : ')) or 
    user_cols=int(input('ncols : '))
    '''
    
    # create board
    b=Board(user_rows,user_cols)

    # run first iteration
    b.draw_board()
    
    
    if autorun:
        import time

        # run till end
        should_continue=True # initialize to run while loop once
        while should_continue:
            should_continue=b.update_board()
            b.draw_board()
            time.sleep(1)

    else:
        # update on on user input
        user_action=''
        should_continue=True # initialize to run while loop once
        while user_action!='q' and should_continue:
            user_action = input('q to quit:')
            
            should_continue=b.update_board()
            b.draw_board()

main(10,10,True)

b=Board()
b=Board(20,20)
b._nrow,b._ncol
b._grid

[1,2,3,4,5,6]

...
x..
...