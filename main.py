import pygame
import tkinter
from tkinter import messagebox


# I am not sure if my game_init solution is the best solution, but it definitely helps to fight the clutter
# That some of my function calls have had
# It also helps me to only have one part of the code that I need to change for options like colour and size
class GameInitialization(object):
    width = 800
    height = width
    screen_size = (width, height)

    rows = 50
    columns = rows
    axis_length = (rows, columns)

    size_between_rows = screen_size[0] // rows
    size_between_columns = screen_size[1] // columns

    color_window = (100, 100, 100)
    color_lines = (60, 60, 60)
    color_live_cells = (150, 150, 0)

    game_started = False
    exit_program = False
    reset_initiated = False

    mouse_button_pressed = False
    set_cell_status_live = True

    # TODO: Check if that is the right approach
    #  It does look and feel so wrong though
    def set_window(self, window):
        self.window = window

    def set_my_grid(self, my_grid):
        self.my_grid = my_grid

    def set_cell_at_new_mouse_position(self, cell):
        self.cell_at_new_mouse_position = cell

    # TODO: Think about more UI-related functions
    #  Do I want a generation counter, live and dead cell counter? etc...


class Cell(object):
    def __init__(self, position):
        self.position = position
        self.live = False


# Check other possible names for the class Grid and the function draw_grid
class Grid(object):
    def __init__(self, axis_length):
        self.rows = axis_length[0]
        self.columns = axis_length[1]
        self.grid = self.create_grid()  # Careful, grid is used like this: self.grid[y][x]
        self.live_cells = set()

        self.cells_touched_by_life = list()
        self.cells_to_be_born = set()
        self.cells_about_to_die = set()

    def create_grid(self):
        grid = [[Cell((x, y)) for x in range(self.columns)] for y in range(self.rows)]
        return grid

    def set_cell_live(self, position):
        cell = self.grid[position[1]][position[0]]
        cell.live = True
        self.live_cells.add(cell)

    def set_cell_dead(self, position):
        cell = self.grid[position[1]][position[0]]
        # Maybe check if the cell was already dead
        # Because then this method call should not be happening
        cell.live = False
        # x.remove() will throw an error when the item is not in the set
        # Not sure if I want to handle such an error
        self.live_cells.discard(cell)

    def get_live_cells_set(self):
        return self.live_cells

    def get_neighbours(self, game_init, cell):
        position = cell.position
        neighbours = set()

        for y_modifier in range(-1, 2):
            for x_modifier in range(-1, 2):
                if x_modifier == 0 and y_modifier == 0:
                    continue

                if self.is_neighbour_possible(game_init, cell, x_modifier, y_modifier):
                    neighbours.add(
                        self.grid[position[1] + y_modifier][position[0] + x_modifier]
                    )

        return neighbours


    def is_neighbour_possible(self, game_init, cell, x_modifier, y_modifier):
        position = cell.position
        # X
        if position[0] + x_modifier > game_init.rows - 1:
            return False
        if position[0] + x_modifier < 0:
            return False

        # Y
        if position[1] + y_modifier > game_init.rows - 1:
            return False
        if position[1] + y_modifier < 0:
            return False

        return True

    def check_neighbours_status(self, neighbours):
        live_counter = 0
        for neighbour in neighbours:
            if neighbour.live:
                live_counter = live_counter + 1
            else:
                self.cells_touched_by_life.append(neighbour)
        return live_counter


    def check_survival(self, live_counter):
        if live_counter == 2 or live_counter == 3:
            return True
        else:
            return False

    def check_reproduction(self):
        cells_touched_by_life_no_duplicates = list(set(self.cells_touched_by_life))
        for cell in cells_touched_by_life_no_duplicates:
            if self.cells_touched_by_life.count(cell) == 3:
                self.cells_to_be_born.add(cell)

    def manage_live_and_dead_cells(self):
        for cell in self.cells_to_be_born:
            self.set_cell_live(cell.position)

        for cell in self.cells_about_to_die:
            self.set_cell_dead(cell.position)

        self.cells_touched_by_life.clear()
        self.cells_to_be_born.clear()
        self.cells_about_to_die.clear()

    def check_rules(self, game_init):
        for cell in self.live_cells:
            neighbours = self.get_neighbours(game_init, cell)
            live_counter = self.check_neighbours_status(neighbours)
            if not self.check_survival(live_counter):
                self.cells_about_to_die.add(cell)

        self.check_reproduction()
        self.manage_live_and_dead_cells()

    def reset_game(self):
        current_live_cells = self.live_cells.copy()
        for cell in current_live_cells:
            self.set_cell_dead(cell.position)

        self.cells_touched_by_life = list()
        self.cells_to_be_born = set()
        self.cells_about_to_die = set()


def draw_live_cells(window, my_grid, game_init):
    color_live_cells = game_init.color_live_cells
    size_between_rows = game_init.size_between_rows
    size_between_columns = game_init.size_between_columns

    live_cells_set = my_grid.get_live_cells_set()
    for cell in live_cells_set:
        x_start = cell.position[0] * size_between_columns + 1
        y_start = cell.position[1] * size_between_rows + 1

        width = size_between_columns - 1
        height = size_between_rows - 1

        pygame.draw.rect(window,
                         color_live_cells,
                         (
                             x_start, y_start,
                             width, height
                         ))


def draw_border(window, game_init):
    screen_size = game_init.screen_size
    color_lines = game_init.color_lines
    # Upper left corner to the upper right corner
    pygame.draw.line(window, color_lines, (0, 0), (screen_size[0], 0))
    # Upper left corner to the lower left corner
    pygame.draw.line(window, color_lines, (0, 0), (0, screen_size[1]))
    # Lower right corner to the upper right corner
    pygame.draw.line(window, color_lines, (screen_size[0], screen_size[1]), (screen_size[0], 0))
    # Lower right corner to the lower left corner
    pygame.draw.line(window, color_lines, (screen_size[0], screen_size[1]), (0, screen_size[1]))


def draw_grid(window, game_init):
    screen_size = game_init.screen_size
    rows = game_init.rows
    columns = game_init.columns
    size_between_rows = game_init.size_between_rows
    size_between_columns = game_init.size_between_columns
    color_lines = game_init.color_lines

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


def get_grid_position(game_init, mouse_pos):
    position = [0, 0]
    corrected_mouse_pos = list()
    # TODO: Remove this correction as it is not actually needed
    # If the mouse is held and dragged over the border
    # X
    if mouse_pos[0] < 0:
        corrected_mouse_pos.append(0)
    elif mouse_pos[0] > game_init.width:
        corrected_mouse_pos.append(game_init.width)
    else:
        corrected_mouse_pos.append(mouse_pos[0])
    # Y
    if mouse_pos[1] < 0:
        corrected_mouse_pos.append(0)
    elif mouse_pos[1] > game_init.width:
        corrected_mouse_pos.append(game_init.height)
    else:
        corrected_mouse_pos.append(mouse_pos[1])

    # Actual pixel position to grid position calculation
    position[0] = corrected_mouse_pos[0] // game_init.size_between_rows
    position[1] = corrected_mouse_pos[1] // game_init.size_between_columns

    return tuple(position)


# While in running pygame one of the 4 pygame.even.X functions HAS to be called
# Else the OS will think that the game has crashed
# You should also implement the QUIT event first, so that you can comfortably quit the project
def event_handler(game_init):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_init.game_started = False
            game_init.exit_program = True
            break
        # TODO: Test if keys has to be outside of the for loop
        keys = pygame.key.get_pressed()

        if keys[pygame.K_r]:
            game_init.reset_initiated = True
            game_init.game_started = False
            game_init.mouse_button_pressed = False
            break

        elif keys[pygame.K_SPACE]:
            # TODO: Test this with 'not' instead of '^='
            #  That should be a better Python style I guess
            game_init.game_started ^= True
            game_init.mouse_button_pressed = False

        # TODO: careful, sometimes when I often clicked with the mouse, the next spacebar input was not read
        #  If the time between the click and the spacebar was too small

        if not game_init.game_started:
            if event.type == pygame.MOUSEBUTTONUP:
                game_init.mouse_button_pressed = False
                # I think I do not have to, but should I reset the other flags when mouse_button goes up ?
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid_position = get_grid_position(game_init, event.dict["pos"])
                game_init.mouse_button_pressed = True
                process_cell_conversion(game_init, grid_position, True)

            if event.type == pygame.MOUSEMOTION and game_init.mouse_button_pressed:
                grid_position = get_grid_position(game_init, event.dict["pos"])
                process_cell_conversion(game_init, grid_position, False)


# TODO: I probably should think about which functions I want to be methods and vice versa
def process_cell_conversion(game_init, grid_position, mouse_button_down):
    if not game_init.mouse_button_pressed:
        print("ERROR: process_cell_conversion() called without 'mouse_button_pressed' flag begin true")
        return

    grid = game_init.my_grid.grid
    cell = grid[grid_position[1]][grid_position[0]]

    if mouse_button_down:
        game_init.set_cell_status_live = not cell.live
        game_init.set_cell_at_new_mouse_position(cell)
    else:
        # Check if the pixel-position is still inside the clicked cell
        if game_init.cell_at_new_mouse_position == cell:
            return
        else:
            game_init.set_cell_at_new_mouse_position(cell)

    # Compare cell status
    # Change if needed
    if game_init.set_cell_status_live:
        if not cell.live:
            game_init.my_grid.set_cell_live(cell.position)
    else:
        if cell.live:
            game_init.my_grid.set_cell_dead(cell.position)


def redraw_window(window, my_grid, game_init):
    window.fill(game_init.color_window)
    draw_grid(window, game_init)
    draw_border(window, game_init)
    draw_live_cells(window, my_grid, game_init)

    pygame.display.update()


def activate_still_lifes(my_grid):
    # Block
    my_grid.set_cell_live((3, 3))
    my_grid.set_cell_live((3, 4))
    my_grid.set_cell_live((4, 3))
    my_grid.set_cell_live((4, 4))
    # Bee-hive
    my_grid.set_cell_live((10, 10))
    my_grid.set_cell_live((11, 10))
    my_grid.set_cell_live((9, 11))
    my_grid.set_cell_live((12, 11))
    my_grid.set_cell_live((10, 12))
    my_grid.set_cell_live((11, 12))
    # Loaf
    my_grid.set_cell_live((20, 20))
    my_grid.set_cell_live((21, 20))
    my_grid.set_cell_live((19, 21))
    my_grid.set_cell_live((22, 21))
    my_grid.set_cell_live((20, 22))
    my_grid.set_cell_live((22, 22))
    my_grid.set_cell_live((21, 23))
    # Boat
    my_grid.set_cell_live((30, 30))
    my_grid.set_cell_live((31, 30))
    my_grid.set_cell_live((30, 31))
    my_grid.set_cell_live((32, 31))
    my_grid.set_cell_live((31, 32))
    # Tub
    my_grid.set_cell_live((40, 40))
    my_grid.set_cell_live((39, 41))
    my_grid.set_cell_live((41, 41))
    my_grid.set_cell_live((40, 42))


def activate_oscillators(my_grid):
    # Blinker (period 2)
    my_grid.set_cell_live((13, 3))
    my_grid.set_cell_live((13, 4))
    my_grid.set_cell_live((13, 5))
    # Toad (period 2)
    my_grid.set_cell_live((20, 10))
    my_grid.set_cell_live((21, 10))
    my_grid.set_cell_live((22, 10))
    my_grid.set_cell_live((19, 11))
    my_grid.set_cell_live((20, 11))
    my_grid.set_cell_live((21, 11))
    # Beacon (period 2)
    my_grid.set_cell_live((40, 30))
    my_grid.set_cell_live((41, 30))
    my_grid.set_cell_live((40, 31))
    my_grid.set_cell_live((42, 33))
    my_grid.set_cell_live((43, 33))
    my_grid.set_cell_live((43, 32))


# TODO: center this window on the actual pygame-window
def welcome_window():
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()  # Hides the main tk window
    subject = "Important information"
    content = "Thanks for playing this game!" \
              "\n\n" \
              "How to play?" \
              "\n\n" \
              "There are 3 rules that decide what happens in the game." \
              "\n1. If a cell has 2 or 3 neighbours it will survive (next generation)" \
              "\n2. If a cell has less than 2 (underpopulation)." \
              "\n   or more than 3 (overpopulation) cells nearby it dies." \
              "\n3. Any dead cell with exactly 3 neighbours will become live (reproduction)." \
              "\n\n" \
              "Hotkeys:" \
              "\nUse the mouse and click on cells to set them live" \
              "\nPress 'spacebar' to start and pause the simulation" \
              "\nPress 'r' to reset the game and open this window once again" \
              "\n\n" \
              "Pressing on 'Ok' will start the game!"

    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    # TODO: Find out which exceptions could occur here and further
    #  specify them, so that this try_except clause is not too broad
    except:
        pass


def main():
    # TODO: center the pygame window on screen when it starts
    pygame.init()
    game_init = GameInitialization()

    # TODO: Check if this is the right approach
    window = pygame.display.set_mode(game_init.screen_size)
    game_init.set_window(window)
    my_grid = Grid(game_init.axis_length)
    game_init.set_my_grid(my_grid)

    # TODO: remove this test part, after user-input implementation
    #  Or maybe implement a way to choose these as presets in the pre-phase
    # Still lifes
    activate_still_lifes(my_grid)
    # Oscillators
    activate_oscillators(my_grid)
    # Corner test
    my_grid.set_cell_live((0, 0))
    my_grid.set_cell_live((game_init.columns - 1, 0))
    my_grid.set_cell_live((0, game_init.rows - 1))
    my_grid.set_cell_live((game_init.columns - 1, game_init.rows - 1))

    my_grid.set_cell_live((5, 5))
    my_grid.set_cell_live((5, 6))
    my_grid.set_cell_live((6, 5))
    my_grid.set_cell_live((6, 6))

    redraw_window(window, my_grid, game_init)

    # Not sure if I should use tkinter or try it with pygame!
    welcome_window()

    loop_counter = 0

    # TODO: Maybe add the program_response_time and cell_activity_delay_factor to game_init
    #  Also maybe change that ridiculous long names to something shorter
    program_response_time = 5
    cell_activity_delay_factor = 100

    while not game_init.exit_program:
        # If pygame.time.wait(x) is not accurate enough, try pygame.time.delay(x)
        pygame.time.wait(program_response_time)
        event_handler(game_init)

        if game_init.game_started:
            loop_counter = loop_counter + 1
            if loop_counter == cell_activity_delay_factor:
                loop_counter = 0
                my_grid.check_rules(game_init)

        if game_init.reset_initiated:
            game_init.reset_initiated = False
            my_grid.reset_game()
            redraw_window(window, my_grid, game_init)
            welcome_window()
            continue

        redraw_window(window, my_grid, game_init)

    pygame.quit()
    exit()


main()
