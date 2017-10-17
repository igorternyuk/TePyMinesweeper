from views.view import*
    
model = MinesweeperModel()
controller = MinesweeperController( model );
view = MinesweeperView( model, controller )
view.mainloop()
