from models.model import*            


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
 
