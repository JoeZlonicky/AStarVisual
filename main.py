import pygame
import sys
import math


class AStarVisual:
    """ Visualizes the A* pathfind algorithm using an inputted map.
        To run, redirect stdin to map.txt """
    BLOCK_CHAR = '#'
    EMPTY_CHAR = '.'
    START_CHAR = 'A'
    END_CHAR = 'B'
    BG_COLOR = (36, 34, 52)
    BLOCK_COLOR = (74, 84, 98)
    LINE_COLOR = (51, 57, 65)
    PATH_COLOR = (156, 219, 67)
    START_COLOR = (89, 193, 53)
    END_COLOR = (180, 32, 42)
    BORDER_WIDTH = 1
    CELL_SIZE = 30
    FPS = 30

    def __init__(self):
        """ Start a new visualization """
        self.size = 0
        self.map = []
        self.start = None
        self.end = None
        self.read_map()

        self.screen = pygame.display.set_mode((self.size * self.CELL_SIZE + (self.size + 1) * self.BORDER_WIDTH,
                self.size * self.CELL_SIZE + (self.size + 1) * self.BORDER_WIDTH))
        pygame.display.set_caption("AStarVisual")
        self.clock = pygame.time.Clock()
        self.queue = []
        self.path = []
        self.cost_to_pos = {}
        self.previous = {}
        self.done = False
        self.begin()

    def read_map(self):
        """ Get map from stdin. Expects first line to be the size of the map 
                and the following lines to be the map itself """
        input = list(sys.stdin)
        self.size = int(input[0])
        self.map = input[1:]
        for i in range(len(self.map)):
            if 'A' in self.map[i]:
                self.start = (self.map[i].index(self.START_CHAR), i)
            if 'B' in self.map[i]:
                self.end = (self.map[i].index(self.END_CHAR), i)

    def begin(self):
        """ Add start cell and begin loop """
        self.queue.append((self.start, 0.0))
        self.cost_to_pos[self.start] = 0
        self.loop()

    def loop(self):
        """ Handle events, apply algorithm and draw to screen """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            if not self.done:
                self.update_path()
                self.algorithm()

            self.screen.fill(self.LINE_COLOR)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def algorithm(self):
        """ Apply A* """
        current = self.get_next_cell()
        if not current or current == self.end:
            self.done = True
            return

        # Add neighbors to queue
        for neighbor in self.get_neighbors(current):
            # Don't add wall cells
            if self.map[current[1]][current[0]] == self.BLOCK_CHAR:
                break

            # Only add if not visited or a cheaper path has been found
            cost = self.cost_to_pos[current] + 1
            if neighbor not in self.cost_to_pos or cost < self.cost_to_pos[neighbor]:
                self.cost_to_pos[neighbor] = cost
                self.previous[neighbor] = current

                # Add to queue based on priority (in this case how close it is to end)
                distance = math.sqrt((self.end[1] - neighbor[1]) ** 2 + (self.end[0] - neighbor[0]) ** 2)
                self.queue.append((neighbor, distance))

    def get_next_cell(self):
        """ Get the highest priority cell """
        if len(self.queue) == 0:
            return
        val = self.peek_queue()
        self.queue.remove(val)
        return val[0]

    def peek_queue(self):
        """ Return the highest priority cell as a tuple: ((x, y), priority) """
        if len(self.queue) == 0:
            return
        max_priority = self.queue[0][1]
        max_priority_position = 0
        for i in range(0, len(self.queue)):
            if self.queue[i][1] < max_priority:
                max_priority = self.queue[i][1]
                max_priority_position = i
        val = self.queue[max_priority_position]
        return val

    def get_neighbors(self, pos):
        """ Get all adjacent cells as a list """
        neighbors = []
        if pos[0] + 1 < self.size:
            neighbors.append((pos[0] + 1, pos[1]))
        if pos[0] - 1 >= 0:
            neighbors.append((pos[0] - 1, pos[1]))
        if pos[1] + 1 < self.size:
            neighbors.append((pos[0], pos[1] + 1))
        if pos[1] - 1 >= 0:
            neighbors.append((pos[0], pos[1] - 1))
        return neighbors

    def update_path(self):
        """ Update the cells that are in the path """
        if len(self.queue) == 0:
            return
        self.path[:] = []
        current = self.peek_queue()[0]
        while current in self.previous:
            self.path.append(current)
            current = self.previous[current]

    def draw_board(self):
        """ Draw map to screen """
        for i in range(self.size):
            for k in range(self.size):
                left = k * self.CELL_SIZE + (k+1) * self.BORDER_WIDTH
                top = i * self.CELL_SIZE + (i+1) * self.BORDER_WIDTH
                rect = pygame.Rect(left, top, self.CELL_SIZE, self.CELL_SIZE)
                color = self.BG_COLOR
                if self.map[i][k] == self.BLOCK_CHAR:
                    color = self.BLOCK_COLOR
                elif self.map[i][k] == self.START_CHAR:
                    color = self.START_COLOR
                elif self.map[i][k] == self.END_CHAR:
                    color = self.END_COLOR
                elif (k, i) in self.path:
                    color = self.PATH_COLOR
                pygame.draw.rect(self.screen, color, rect)


if __name__ == '__main__':
    AStarVisual()
