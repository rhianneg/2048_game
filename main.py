import time
import tkinter as tk # For Python 3
import tkinter.messagebox as messagebox
from gamepanel import GamePanel

class Game:
    '''The main game class which is the controller of the whole game.'''
    def __init__(self, grid, panel):
        self.grid = grid
        self.panel = panel
        self.start_cells_num = 2
        self.over = False
        self.won = False
        self.keep_playing = False

    def is_game_terminated(self):
        return self.over or (self.won and (not self.keep_playing))

    def start(self):

        #This function is used to start the game. 
        # It calls the add_start_cells method to add some initial cells to the grid,
        # and then sets up an event handler for key presses, which will be used to control the game. 
        # Finally, it starts the main event loop of the game.

        global start_time 
        start_time = time.time()

        self.add_start_cells()
        self.panel.paint()
        self.panel.root.bind('<Key>', self.key_handler)
        self.panel.root.mainloop()

    def add_start_cells(self):

        #The add_start_cells method simply adds a certain number of random cells to the grid.

        for i in range(self.start_cells_num):
            self.grid.random_cell()

    def can_move(self):
        return self.grid.has_empty_cells() or self.grid.can_merge()

    def key_handler(self, event):
        #This function is the event handler for key presses. 
        # It uses the value of the pressed key to determine which direction the 
        # player wants to move the tiles. It then calls one of the up, left, down, 
        # or right methods to move the tiles in the corresponding direction. 
        # After each move, it checks if the game has been won or lost, and 
        # if the game is not over, it adds a new random cell to the grid
        
        if self.is_game_terminated():
            return

        self.grid.clear_flags()
        key_value = event.keysym
        print('{} key pressed'.format(key_value))
        if key_value in GamePanel.UP_KEYS:
            self.up()
        elif key_value in GamePanel.LEFT_KEYS:
            self.left()
        elif key_value in GamePanel.DOWN_KEYS:
            self.down()
        elif key_value in GamePanel.RIGHT_KEYS:
            self.right()
        else:
            pass

        self.panel.paint()
        print('Score: {}'.format(self.grid.current_score))
        if self.grid.found_2048():
            self.you_win()
            if not self.keep_playing:
                return

        if self.grid.moved:
            self.grid.random_cell()

        self.panel.paint()
        if not self.can_move():
            global round_elapsed_time
            self.over = True
            elapsed_time = time.time() - start_time
            round_elapsed_time = round(elapsed_time)
            print("Time elapsed: ", round_elapsed_time)
            self.game_over()

    def you_win(self):
        if not self.won:
            self.won = True
            print('You Win!')
            w_msg = 'You Won in ' + round_elapsed_time + ' seconds! Do you want to continue the 2048 game?'
            if messagebox.askyesno('2048', w_msg):
                self.keep_playing = True

    def game_over(self):
        print('Game over!')
        l_msg = 'Oops! Game over! You took ' + str(round_elapsed_time) + ' seconds.'
        messagebox.showinfo('2048', l_msg )


    #The up, left, down, and right methods are used to move the tiles in the corresponding directions. 
    # They all work by manipulating the grid in some way (e.g., transposing it, reversing it, etc.),
    #  and then using the left_compress and left_merge methods to move and merge the tiles.
    
    def up(self):
        self.grid.transpose()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.transpose()

    def left(self):
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()

    def down(self):
        self.grid.transpose()
        self.grid.reverse()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.reverse()
        self.grid.transpose()

    def right(self):
        self.grid.reverse()
        self.grid.left_compress()
        self.grid.left_merge()
        self.grid.moved = self.grid.compressed or self.grid.merged
        self.grid.left_compress()
        self.grid.reverse()