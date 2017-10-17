from tkinter import*
from tkinter.messagebox import *
import random

class MineSweeperCell:
    def __init__( self, row, column ):
        self.row = row
        self.column = column
        self.state = 'closed'
        self.is_mined = False
        self.num_mines_around = 0
        
    markSequence = [ 'closed', 'flagged', 'questioned' ]

    # right mouse button click
    def next_mark( self ):
        if self.state in self.markSequence:
            index = self.markSequence.index( self.state )
            self.state = self.markSequence[(index + 1) % len(self.markSequence)]


    def open( self ):
        if self.state != 'flagged':
            self.state = 'opened'
            

class MinesweeperModel:
    def __init__( self ):
        self.start_new_game()


    def min_row_count( self ):
        return 9


    def max_row_count( self ):
        return 30


    def min_column_count( self ):
        return 9


    def max_column_count( self ):
        return 30


    def min_mine_count( self ):
        return 10


    def max_mine_count( self ):
        return 500

    
    def start_new_game( self, num_rows = 9, num_columns = 9, num_mines = 10 ):
        #check if input parameter are in acceptable ranges
        if num_rows in range( self.min_row_count(), self.max_row_count() + 1 ):
            self.__num_rows = num_rows

        if num_columns in range ( self.min_column_count(), self.max_column_count() + 1):
            self.__num_columns = num_columns

        if (num_mines < self.__num_rows * self.__num_columns and
            num_mines in range( self.min_mine_count(), self.max_mine_count() + 1)):
            self.__num_mines = num_mines
        else:
            self.__num_mines = int(0.8 * self.__num_rows * self.__num_columns)
        
        self.is_first_step = True
        self.__is_game_over = False
        self.grid = []
        for r in range( self.__num_rows ):
            row = []
            for c in range( self.__num_columns ):
                row.append( MineSweeperCell( r, c ) )
            self.grid.append( row )


    def row_count( self ):
        return self.__num_rows


    def column_count( self ):
        return self.__num_columns


    def mine_count( self ):
        return self.__num_mines

    
    def __is_coords_in_range( self, row, column ):
        return (row >= 0 and row < self.__num_rows and column >= 0 and
                column < self.__num_columns)
    
    
    def get_cell( self, r, c ):
        if self.__is_coords_in_range( r, c ):
            return self.grid[ r ][ c ]
        else:
            return None
        

    def is_win( self ):
        for r in range( self.__num_rows ):
            for c in range( self.__num_columns ):
                cell = self.grid[r][c]
                if (not cell.is_mined and ( cell.state == 'closed' or
                                           cell.state == 'questioned' )):
                    return False
        return True


    def is_game_over( self ):
        return self.__is_game_over


    def __get_cell_neighbours( self, r, c ):
        neighbours = []
        for dr in range( -1, 2 ):
            for dc in range( -1, 2 ):
                if dr == 0 and dc == 0:
                    continue
                nr = r + dr
                nc = c + dc
                if self.__is_coords_in_range( nr, nc ):
                    neighbours.append( self.grid[ nr ][ nc ] )
        return neighbours


    def __count_mines_around( self, row, column ):
        #print("Counting mines around ... ")        
        neighbours = self.__get_cell_neighbours( row, column )
        #print(" Clicked cell has ", len(neighbours), " neighbours")
        count = 0
        for cell in neighbours:
            if cell.is_mined:
                count += 1
        return count


    def next_cell_mark( self, row, column ):
        cell = self.get_cell( row, column )
        if cell:
            cell.next_mark()


    def __create_mine_field( self ):
        for m in range( self.__num_mines ):
            while True:
                rand_row = random.choice( range( self.__num_rows ) )
                rand_col = random.choice( range( self.__num_columns ) )
                rand_cell = self.get_cell( rand_row, rand_col )
                if rand_cell.state != 'opened' and not rand_cell.is_mined:
                    rand_cell.is_mined = True
                    break;


    def open_cell( self, row, column ):
        cell = self.get_cell( row, column )

        cell.open()

        if cell.is_mined:
            self.__is_game_over = True

        if self.is_first_step:
            self.is_first_step = False
            self.__create_mine_field()

        cell.num_mines_around = self.__count_mines_around( row, column )
        #print("There are ", cell.num_mines_around, " mines around clicked cell")
        if cell.num_mines_around == 0:
            neighbours = self.__get_cell_neighbours( row, column )
            for cell in neighbours:
                if cell.state == 'closed':
                    self.open_cell( cell.row, cell.column )


    def print_to_console( self ):
        for r in range( self.__num_rows ):
            line = []
            for c in range( self.__num_columns ):
                
                cell = self.get_cell( r, c )
                if cell.is_mined:
                    line.append("X")
                else:
                    line.append("")
            print(line)
            


class MinesweeperController:
    def __init__( self, model ):
        self.__model = model
        

    def setView( self, view ):
        self.view = view


    def __check_win( self ):
        if self.__model.is_win():
            self.view.show_win_message()
            self.start_new_game()
        elif self.__model.is_game_over():
            self.view.show_game_over_message()
            self.start_new_game()
            

    def start_new_game( self ):
        print("Start new game")
        game_settings = self.view.get_user_settings()
        try:
            # starred symbol means tuple unpacking
            self.__model.start_new_game( *map(int, game_settings))
        except:
            self.__model.start_new_game( self.__model.row_count(), self.__model.column_count(),
                                       self.__model.mine_count() )
        self.view.create_field()


    def on_left_click( self, row, column ):
        print("Left click row = ", row, " col = ", column )
        if self.__model.get_cell( row, column ).state == 'flagged':
            return
        self.__model.open_cell( row, column )
        self.view.sync_with_model()
        self.__check_win()

    def on_right_click( self, row, column ):
        print("Right click row = ", row, " col = ", column )
        self.__model.next_cell_mark( row, column )
        self.view.sync_with_model()
        self.__check_win()
 

class MinesweeperView( Tk ):
    
    def __init__( self, model, controller, parent = None ):
        Tk.__init__( self, parent )
        self.title("Minesweeper")
        #self.geometry("800x600+0+0")        
        self.__model = model
        self.__controller = controller
        self.__row_count = StringVar()
        self.__col_count = StringVar()
        self.__mine_count = StringVar()
        self.__field = None
        self.__controller.setView( self )        
        self.create_field()     

        self.panel = Frame( self, width = 300, height = 100, bg = "light green",
                            bd = 6, relief = SUNKEN )
        self.panel.pack( side = BOTTOM)

        self.lbl_mine_count = Label( self.panel, font=('Tahoma', 14, 'bold' ),
                                     fg = 'blue', bg = "light green",
                                     text = "Field size: " )
        self.lbl_mine_count.grid( row = 0, column = 0 )

        self.spiner_field_width = Spinbox(
                                           self.panel,
                                           from_ = self.__model.min_column_count(),
                                           to = self.__model.max_column_count(),
                                           width = 5, font=('Tahoma', 14, 'bold'),
                                           textvariable = self.__col_count
                                         )
        self.spiner_field_width.grid( row = 0, column = 1 )

        self.lbl_x = Label( self.panel, font=('Tahoma', 14, 'bold'),
                            fg = 'blue', bg = "light green",
                            text = " X " )
        self.lbl_x.grid( row = 0, column = 2 )

        self.spiner_field_height = Spinbox(
                                            self.panel,
                                            from_ = self.__model.min_row_count(),
                                            to = self.__model.max_row_count(),
                                            width = 5,
                                            font=('Tahoma', 14, 'bold'),
                                            textvariable = self.__row_count
                                          )
        self.spiner_field_height.grid( row = 0, column = 3 )

        self.lbl_mine_count = Label( self.panel, font=('Tahoma', 14, 'bold' ),
                                     fg = 'blue', bg = "light green",
                                     text = "Mine count: " )
        self.lbl_mine_count.grid( row = 0, column = 4)

        self.spiner_mine_count = Spinbox(
                                          self.panel,
                                          from_ = self.__model.min_mine_count(),
                                          to = self.__model.max_mine_count(),
                                          width = 5, font=('Tahoma', 14, 'bold'),
                                          textvariable = self.__mine_count
                                        )
        self.spiner_mine_count.grid( row = 0, column = 5 )



        self.btn_new_game = Button( self.panel, font=('Tahoma', 14, 'bold'),
                                    bg="Powder blue", text = "New game",
                                    fg = 'blue', bd = 4, relief = RAISED,
                                    command = self.__controller.start_new_game )
        self.btn_new_game.grid(  row = 0, column = 6 )


    def get_user_settings( self ):
        return self.__row_count.get(), self.__col_count.get(), self.__mine_count.get()
        
    def show_win_message( self ):
        showinfo( 'Congratulations!', 'You won!!!')


    def show_game_over_message( self ):
        showinfo( 'Game over!', 'You lost!')


    def create_field( self ):
        #print("create_field")
        if not self.__field is None:
            self.__field.destroy()
        self.__row_count.set( self.__model.row_count() )
        self.__col_count.set( self.__model.column_count() )
        self.__mine_count.set( self.__model.mine_count() )

        self.__field = Frame( self )
        self.__field.pack()
        self.buttons_grid = []
        for r in range( self.__model.row_count() ):
            line = Frame( self.__field )
            line.pack( side = TOP )
            self.buttons_row = []
            for c in range( self.__model.column_count() ):
                btn = Button(
                        line,
                        padx = 0,
                        pady = 0,
                        width = 2,
                        height = 1,
                        bd = 4,
                        relief = RAISED,
                        bg = 'powder blue',
                        font=('Consolas', 11, 'bold')
                    )
                btn.pack( side = LEFT )
                btn.bind( '<Button-1>', lambda e, row = r, col = c:
                          self.__controller.on_left_click( row, col ) )
                btn.bind( '<Button-3>', lambda e, row = r, col = c:
                          self.__controller.on_right_click( row, col ), '+' )
                self.buttons_row.append( btn )
            self.buttons_grid.append( self.buttons_row )
            

    def get_cell_color( self, mines_around ):
        if mines_around == 1:
            return 'dark red'
        elif mines_around == 2:
            return 'dark green'
        elif mines_around == 3:
            return 'Dark Violet'
        elif mines_around == 4:
            return 'Brown'
        elif mines_around == 5:
            return 'Saddle Brown'
        elif mines_around == 6:
            return 'Olive Drab'
        elif mines_around == 7:
            return 'Light Sea Green'
        elif mines_around == 8:
            return 'Medium Blue'

    
    def sync_with_model( self ):
        #self.model.print_to_console()
        for r in range( self.__model.row_count() ):
            for c in range ( self.__model.column_count() ):
                cell = self.__model.get_cell( r, c )
                if cell:
                    btn = self.buttons_grid[ r ][ c ]

                    if self.__model.is_game_over() and cell.is_mined:
                        btn.config( bg = 'black', fg = 'black', text = '')

                    if cell.state == 'closed':
                        btn.config( text = '' )
                    elif cell.state == 'flagged':
                        btn.config( text = 'F', fg = 'red' )
                    elif cell.state == 'questioned':
                        btn.config( text = '?', fg = 'red' )
                    elif cell.state == 'opened':
                        btn.config(bg = 'white', relief = SUNKEN )
                        if cell.is_mined:
                            btn.config( text = '', bg = 'red' )
                        else:
                            if cell.num_mines_around > 0:
                                btn.config( text = str(cell.num_mines_around),
                                            fg = self.get_cell_color(cell.num_mines_around) )
                            else:
                                btn.config( text = '' )

    
model = MinesweeperModel()
controller = MinesweeperController( model );
view = MinesweeperView( model, controller )
view.mainloop()
