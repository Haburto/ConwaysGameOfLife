import pygame


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
    # Still lifes
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

    # Oscillators
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

    # TODO: change the following solution to something not that stupid
    first_loop = True
    running = True
    while running:
        # TODO: is there a better alternative for pygame.time.delay(x)?
        # 500 ms seem good for 'gameplay', 1000+ is good for testing the logic
        pygame.time.delay(500)

        # While in running pygame one of the 4 pygame.even.X functions HAS to be called
        # Else the OS will think that the game has crashed
        # You should also implement the QUIT event first, so that you can comfortably quit the project
        event_handler()
        if not first_loop:
            my_grid.check_rules()

        redraw_window(window, screen_size, rows, columns, my_grid,color_window, color_lines, color_live_cells)
        first_loop = False

    pygame.quit()
    exit()


main()
