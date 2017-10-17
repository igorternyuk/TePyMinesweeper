from tkinter import*
from tkinter.messagebox import *

from models.model import*
from controllers.controller import*


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
