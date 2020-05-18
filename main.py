import pygame
import tkinter
from tkinter import messagebox


class Cell(object):
    def __init__(self, position):
        self.position = position
        self.live = False


# Check other possible names for the class Grid and the function draw_grid
class Grid(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
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

    def get_neighbours(self, cell):
        position = cell.position
        neighbours = set()
        neighbours.update([
            self.grid[position[1]-1][position[0]-1],  # top - left
            self.grid[position[1]-1][position[0]],  # top - center
            self.grid[position[1]-1][position[0]+1],  # top - right

            self.grid[position[1]][position[0]-1],  # middle - left
            self.grid[position[1]][position[0]+1],  # middle - right

            self.grid[position[1]+1][position[0]-1],  # bottom - left
            self.grid[position[1]+1][position[0]],  # bottom - center
            self.grid[position[1]+1][position[0]+1],  # bottom - right
        ])
        return neighbours

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

    def check_rules(self):
        for cell in self.live_cells:
            neighbours = self.get_neighbours(cell)
            live_counter = self.check_neighbours_status(neighbours)
            if not self.check_survival(live_counter):
                self.cells_about_to_die.add(cell)

        self.check_reproduction()
        self.manage_live_and_dead_cells()


def draw_live_cells(window, my_grid, color_live_cells, size_between_rows, size_between_columns):
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


def draw_border(window, screen_size, color_lines):
    # Upper left corner to the upper right corner
    pygame.draw.line(window, color_lines, (0, 0), (screen_size[0], 0))
    # Upper left corner to the lower left corner
    pygame.draw.line(window, color_lines, (0, 0), (0, screen_size[1]))
    # Lower right corner to the upper right corner
    pygame.draw.line(window, color_lines, (screen_size[0], screen_size[1]), (screen_size[0], 0))
    # Lower right corner to the lower left corner
    pygame.draw.line(window, color_lines, (screen_size[0], screen_size[1]), (0, screen_size[1]))


def draw_grid(window, screen_size, rows, columns, size_between_rows, size_between_columns, color_lines):
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

# TODO: replace the placeholders
def get_grid_position(mouse_pos):
    position = set()
    size_between_rows_PLACEHOLDER = 5
    size_between_columns_PLACEHOLDER = 5
    position[0] = mouse_pos[0] // size_between_columns_PLACEHOLDER
    position[1] = mouse_pos[1] // size_between_rows_PLACEHOLDER


    print("position is:", position)

# While in running pygame one of the 4 pygame.even.X functions HAS to be called
# Else the OS will think that the game has crashed
# You should also implement the QUIT event first, so that you can comfortably quit the project
def event_handler():
    global running
    print("in event_handler()")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        # TODO: Test if keys has to be outside of the for loop
        keys = pygame.key.get_pressed()
        # TODO: Use the mouse and click on cells to set them live
        # TODO: Maybe implement a cell deletion on MOUSE-2 rather than clicking them again
#         in event_handler()
#         in for ...event.get()
#         event < Event(5 - MouseButtonDown
#         {'pos': (267, 277), 'button': 1, 'window': None}) >
#         in for ...event.get()
#         event < Event(6 - MouseButtonUp
#         {'pos': (267, 277), 'button': 1, 'window': None}) >
#         in for ...event.get()
#         event < Event(4 - MouseMotion
#         {'pos': (342, 295), 'rel': (75, 18), 'buttons': (0, 0, 0), 'window': None}) >
#         in event_handler()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("BUTTON DOWN ------------------------------------------")
            # Convert pos into corresponding cell
            # This cell will be set alive
            # Do this until "MOUSEBUTTONUP"
            # So players can click single cells, or 'drawn' multiple cells to set them live
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("BUTTON UP --------------------------------------------")



        # in for ...event.get()
        # event < Event(2 - KeyDown
        # {'unicode': 'r', 'key': 114, 'mod': 0, 'scancode': 19, 'window': None}) >
        # TODO: Press 'spacebar' to start the simulation
        elif keys[pygame.K_SPACE]:
            print("implement key 'space' to start the game")
            pass
        # TODO: Press 'p' to pause the game
        elif keys[pygame.K_p]:
            print("implement key 'p' to pause")
            pass
        # TODO: Press 'r' to reset the game and open this window once again
        elif keys[pygame.K_r]:
            print("implement key 'r' to reset the game")
            pass


def redraw_window(window, screen_size, rows, columns, my_grid, color_window, color_lines, color_live_cells):
    size_between_rows = screen_size[0] // rows
    size_between_columns = screen_size[1] // columns

    window.fill(color_window)
    draw_grid(window, screen_size, rows, columns, size_between_rows, size_between_columns, color_lines)
    draw_border(window, screen_size, color_lines)
    draw_live_cells(window, my_grid, color_live_cells, size_between_rows, size_between_columns)

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
              "\nPress 'spacebar' to start the simulation" \
              "\nPress 'p' to pause the game" \
              "\nPress 'r' to reset the game and open this window once again" \
              "\n\n" \
              "Pressing on 'Ok' will start the game!"

    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# I probably should do the following TO-DO first and after that resuming the position calculation in get_grid_position()
# TODO: Implement a GameIni class or something in that order
#  This class has all the important values and getter methods
#  That way I do not need to use global vars and also the method-calls get way shorter and easier to read
#  It also solves the problem of the current easy missing access to the several options that could be possible

# TODO: implement mouse support

# TODO: implement a pre-game phase (in which the user can choose cells that are live)
# TODO: implement a start button
# TODO: implement a reset-function -> leads to pre-game phase
# TODO: implement a pause-function

# TODO: implement a way to let the user activate the predefined functions (fully implement the hotkeys)

# TODO: implement a way to call the redraw and (maybe) game logic function as often as now BUT handle inputs way more
#  frequent (moving the windows, pressing on x (quit)) for more fluid feeling inputs
def main():
    global running
    pygame.init()

    width = 800
    height = width
    screen_size = (width, height)
    window = pygame.display.set_mode(screen_size)

    rows = 50
    columns = rows
    my_grid = Grid(rows, columns)

    color_window = (100, 100, 100)
    color_lines = (60, 60, 60)
    color_live_cells = (150, 150, 0)

    # TODO: remove this test part, after user-input implementation
    #  Or maybe implement a way to choose these as presets in the pre-phase
    # Still lifes
    activate_still_lifes(my_grid)
    # Oscillators
    activate_oscillators(my_grid)

    redraw_window(window, screen_size, rows, columns, my_grid, color_window, color_lines, color_live_cells)

    # Not sure if I should use tkinter or try it with pygame!
    welcome_window()

    running = True
    while running:
        # TODO: check for a better alternative for pygame.time.delay(x)
        pygame.time.delay(500)
        event_handler()
        my_grid.check_rules()
        redraw_window(window, screen_size, rows, columns, my_grid,color_window, color_lines, color_live_cells)

    pygame.quit()
    exit()


main()
