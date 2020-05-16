import pygame

# TODO: create background with pygame
# TODO: create grid with pygame
# TODO: create class Cell and implement the logic (rules)

# RULES for Conways Game of Life
# A cell has two states 'live' or 'dead'
# A cell interacts with its eight neighbours (horizontally, vertically or diagonally adjacent)

# 1. If a cell has ==2 or ==3 neighbours it survives
# 2. If there are <2 or >3 Cells nearby the cell dies
# 3. If there are ==3 live cells near a dead cells, it becomes live

# TODO: test the wikipedia example patterns


def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break


def main():
    global running
    pygame.init()

    width = 1000
    height = width

    window = pygame.display.set_mode((width, height))

    running = True
    while running:
        # While in running pygame one of the 4 pygame.even.X functions HAS to be called
        # Else the OS will think that the game has crashed
        # You should also implement the QUIT event first, so that you can comfortably quit the project
        event_handler()

    pygame.quit()
    exit()


main()
