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

