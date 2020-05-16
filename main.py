import pygame

# TODO: create class Cell and implement the logic (rules)

# RULES for Conways Game of Life
# A cell has two states 'live' or 'dead'
# A cell interacts with its eight neighbours (horizontally, vertically or diagonally adjacent)

# 1. If a cell has ==2 or ==3 neighbours it survives
# 2. If there are <2 or >3 Cells nearby the cell dies
# 3. If there are ==3 live cells near a dead cells, it becomes live

# TODO: test the wikipedia example patterns


# TODO: create grid with pygame
def draw_grid(window, screen_size, rows, columns):
    size_between_rows = screen_size[0] // rows
    size_between_columns = screen_size[1] // columns
    color_lines = (255, 255, 255)

    for row in range(1, rows + 1):
        pygame.draw.line(window,
                         color_lines,
                         (0, row * size_between_rows),
                         (screen_size[0], row * size_between_rows))

    for column in range(1, columns + 1):
        pygame.draw.line(window,
                         color_lines,
                         (column * size_between_columns, 0),
                         (column * size_between_columns, screen_size[1]))


def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break


def redraw_window(window, screen_size, rows, columns):
    color_window = (0, 0, 0)
    window.fill(color_window)
    draw_grid(window, screen_size, rows, columns)
    pygame.display.update()


# TODO: implement a easy way to change the screen settings
# like row and column count, colors, etc.
def main():
    global running
    pygame.init()

    width = 800
    height = width
    screen_size = (width, height)
    rows = 50
    columns = rows

    window = pygame.display.set_mode(screen_size)

    running = True
    while running:
        # While in running pygame one of the 4 pygame.even.X functions HAS to be called
        # Else the OS will think that the game has crashed
        # You should also implement the QUIT event first, so that you can comfortably quit the project
        event_handler()
        redraw_window(window, screen_size, rows, columns)

    pygame.quit()
    exit()


main()
