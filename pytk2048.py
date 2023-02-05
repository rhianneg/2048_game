from __future__ import print_function

import tkinter as tk # For Python 3
import tkinter.messagebox as messagebox
import sys
import random
import time

from main import Game
from gamepanel import GamePanel

class Grid:
    #Data Structure of the 2048 game

    def __init__(self, n):

        #The __init__(self, n) is the constructor for the class. It initializes the size of the grid 
        # to n and creates an empty grid of n rows and n columns using the generate_empty_grid_box method. 
        # It also initializes some flags that track the state of the grid (e.g., whether it has been compressed, 
        # merged, or moved) and the current score of the game.

        self.size = n
        self.cells = self.generate_empty_grid_box()
        self.compressed = False
        self.merged = False
        self.moved = False
        self.current_score = 0

    def random_cell(self):

        #This function selects a random empty cell in the grid and fills it with either a 2 or a 4 
        #(with a 90% probability of being a 2).

        cell = random.choice(self.retrieve_empty_cells())
        i = cell[0]
        j = cell[1]
        self.cells[i][j] = 2 if random.random() < 0.9 else 4

    def retrieve_empty_cells(self):

        #retrieve_empty_cells(self): This method returns a list of tuples containing the indices of all the empty cells in the grid.

        empty_cells = []
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    empty_cells.append((i, j))
        return empty_cells

    def generate_empty_grid_box(self):
        #This method returns an empty grid of n rows and n columns (i.e., a grid with all cells set to 0).

        return [[0] * self.size for i in range(self.size)]

    def transpose(self):

        #This method transposes the grid (i.e., swaps the rows and columns).

        self.cells = [list(t) for t in zip(*self.cells)]

    def reverse(self):

        # This method reverses the order of the cells in each row of the grid.

        for i in range(self.size):
            start = 0
            end = self.size - 1
            while start < end:
                self.cells[i][start], self.cells[i][end] = \
                    self.cells[i][end], self.cells[i][start]
                start += 1
                end -= 1

    def clear_flags(self):

        #  This method resets the flags that track the state of the grid to 
        # their default values (i.e., sets compressed, merged, and moved to False).

        self.compressed = False
        self.merged = False
        self.moved = False

    def left_compress(self):

        #This method compresses the cells in each row of the grid to the left, moving 
        # all non-zero cells to the leftmost positions and filling the empty cells 
        # on the right with zeros. It sets the compressed flag to Trueif any cells were moved.

        self.compressed = False
        new_grid = self.generate_empty_grid_box()
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                if self.cells[i][j] != 0:
                    new_grid[i][count] = self.cells[i][j]
                    if count != j:
                        self.compressed = True
                    count += 1
        self.cells = new_grid

    def left_merge(self):

        #This method looks for pairs of adjacent cells with the same value in 
        # each row of the grid and merges them by doubling the value of the 
        # leftmost cell and setting the rightmost cell to 0. It sets the merged 
        # flag to True if any cells were merged.

        self.merged = False
        for i in range(self.size):
            for j in range(self.size - 1):
                if self.cells[i][j] == self.cells[i][j + 1] and \
                   self.cells[i][j] != 0:
                    self.cells[i][j] *= 2
                    self.cells[i][j + 1] = 0
                    self.current_score += self.cells[i][j]
                    self.merged = True

    def found_2048(self):

        #This method returns True if the grid contains at least one cell 
        # with a value of 2048 or higher, and False otherwise.

        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] >= 2048:
                    return True
        return False

    def has_empty_cells(self):

        #This method returns True if the grid has at least one empty cell 
        # (i.e., a cell with a value of 0), and False otherwise.
        
        for i in range(self.size):
            for j in range(self.size):
                if self.cells[i][j] == 0:
                    return True
        return False

    def can_merge(self):

        #This method returns True if there are any adjacent cells with the same 
        #value in the grid (either horizontally or vertically), and False otherwise.

        for i in range(self.size):
            for j in range(self.size - 1):
                if self.cells[i][j] == self.cells[i][j + 1]:
                    return True
        for j in range(self.size):
            for i in range(self.size - 1):
                if self.cells[i][j] == self.cells[i + 1][j]:
                    return True
        return False

    def set_cells(self, cells):

        #This method sets the cells of the grid to the values in the cells 
        # parameter (which should be a list of lists).
        self.cells = cells

    def print_grid(self):
        #This method prints the grid to the console, with each row on a separate line and each cell separated by a tab.
        print('-' * 40)
        for i in range(self.size):
            for j in range(self.size):
                print('%d\t' % self.cells[i][j], end='')
            print()
        print('-' * 40)



if __name__ == '__main__':
    size = 4
    grid = Grid(size)
    panel = GamePanel(grid)
    game2048 = Game(grid, panel)
    game2048.start()
    
