from game import Game

game = Game()
while True:
    #game.show_state()
    if game.page == 1:
        game.first_screen()
    if game.page == 2:
        game.second_screen()
    if game.page == 3:
        game.third_screen()
        game.reset()