import pygame

# TODO: test the wikipedia example patterns

# TODO: implement the logic
# RULES for Conways Game of Life
# A cell has two states 'live' or 'dead'
# A cell interacts with its eight neighbours (horizontally, vertically or diagonally adjacent)

# 1. If a cell has ==2 or ==3 neighbours it survives
# 2. If there are <2 or >3 Cells nearby the cell dies
# 3. If there are ==3 live cells near a dead cells, it becomes live
# ----------

# The grid is iterating through every alive cell and does the following:
#       check for rule 1 (next generation)
#       check for rule 2 (under and overpopulation)
#       check for rule 3 (reproduction)

# Rule 1: check the neighbours and act accordingly on the specific cell
# Rule 2: == rule 1
# Maybe create a list with cells that will die and iterate through the list after all rules were calculated (?)
# Not sure how the order should be

# Rule 3: Create a list with cells that have neighbours that are live
# the list should not allow duplicates -> google tuple, list, dict, etc...
# iterate through the list and check for for each cell if rule 3 is applicable


class Cell(object):
    def __init__(self, position):
        self.position = position
        self.live = False


# TODO: implement class Grid
# Check other possible names for the class Grid and the function draw_grid
class Grid(object):
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cell_count = rows + 1 * columns + 1  # Not sure if I need this
        self.grid = self.create_grid()  # Careful, grid is used like this: self.grid[y][x]
        self.live_cells = set()
        self.cells_touched_by_life = set()
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
            self.grid[position[-1]][position[-1]],  # top - left
            self.grid[position[0]][position[-1]],  # top - center
            self.grid[position[1]][position[-1]],  # top - right

            self.grid[position[-1]][position[0]],  # middle - left
            self.grid[position[1]][position[0]],  # middle - right

            self.grid[position[-1]][position[1]],  # bottom - left
            self.grid[position[0]][position[1]],  # bottom - center
            self.grid[position[1]][position[1]],  # bottom - right
        ])
        return neighbours

    def check_neighbours_status(self, neighbours):
        live_counter = 0
        for neighbour in neighbours:
            if neighbour.live:
                live_counter = live_counter + 1
            else:
                self.cells_touched_by_life.add(neighbour)
        return live_counter

    def check_survival(self, live_counter):
        if live_counter == 2 or live_counter == 3:
            return True
        else:
            return False

    def manage_reproduction(self):
        pass

    def check_rules(self):
        for cell in self.live_cells:
            neighbours = self.get_neighbours(cell)
            live_counter = self.check_neighbours_status(neighbours)
            if not self.check_survival(live_counter):
                self.cells_about_to_die.add(cell)

            # Needs the list with cells that are dead but near live cells
            # Do not forget to reset that list in r3
            self.rule_3_reproduction()
            # New idea: use a list that allows duplicates for "touched_by_life" cells
            # Then copy the list and remove the duplicates
            # Iterate through that list and for each item do:
            #       count the number of times these items are in the first list
            #       if it is >=3 (not sure about >, but == 3 is correct)
            #       then the cell will go into a new list

        # List with cells that are about to die -> let them die now
        # cells_about_to_die
        # Set them dead now

        # List with cells that will be live
        # STILL HAS TO BE CREATED
        # Set them live now


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


def event_handler():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break


def redraw_window(window, screen_size, rows, columns, my_grid, color_window, color_lines, color_live_cells):
    size_between_rows = screen_size[0] // rows
    size_between_columns = screen_size[1] // columns

    window.fill(color_window)
    draw_grid(window, screen_size, rows, columns, size_between_rows, size_between_columns, color_lines)
    draw_border(window, screen_size, color_lines)
    draw_live_cells(window, my_grid, color_live_cells, size_between_rows, size_between_columns)

    pygame.display.update()


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

    # TODO: remove this test part, after mouse action implementation
    my_grid.set_cell_live((0, 1))
    my_grid.set_cell_live((3, 5))
    my_grid.set_cell_live((3, 6))
    my_grid.set_cell_live((4, 5))

    clock = pygame.time.Clock()

    running = True
    while running:
        # TODO: alter the following the lines and see which is beneficial for the game!
        pygame.time.delay(50)
        clock.tick(10)

        # While in running pygame one of the 4 pygame.even.X functions HAS to be called
        # Else the OS will think that the game has crashed
        # You should also implement the QUIT event first, so that you can comfortably quit the project
        event_handler()
        redraw_window(window, screen_size, rows, columns, my_grid,color_window, color_lines, color_live_cells)

    pygame.quit()
    exit()


main()
