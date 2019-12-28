import pygame
import sys
import math

BLOCK_CHAR = '#'
EMPTY_CHAR = '.'
START_CHAR = 'A'
END_CHAR = 'B'
BG_COLOR = (0, 0, 0)
BLOCK_COLOR = (255, 255, 255)
LINE_COLOR = (75, 75, 75)
PATH_COLOR = (255, 0, 0)
START_COLOR = (0, 255, 0)
END_COLOR = (0, 0, 255)
BORDER_WIDTH = 1
CELL_SIZE = 30
FPS = 30


class AStarVisual:
    def __init__(self, size, map):
        self.size = size
        self.map = map
        self.start = None
        self.end = None
        self.queue = []
        self.cost_to_pos = {}
        self.previous = {}
        self.screen = pygame.display.set_mode((size * CELL_SIZE + (size + 1) * BORDER_WIDTH,
                size * CELL_SIZE + (size + 1) * BORDER_WIDTH))
        self.clock = pygame.time.Clock()
        self.done = False
        self.path = []
        self.begin()

    def begin(self):
        for i in range(len(self.map)):
            if 'A' in self.map[i]:
                self.start = (self.map[i].index(START_CHAR), i)
            if 'B' in self.map[i]:
                self.end = (self.map[i].index(END_CHAR), i)
        self.queue.append((self.start, 0.0))
        self.cost_to_pos[self.start] = 0
        self.loop()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if not self.done:
                self.update_path()
                self.algorithm()

            self.screen.fill(LINE_COLOR)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

    def algorithm(self):
        current = self.get_next_cell()
        if not current or current == self.end:
            self.done = True
            return

        # Add neighbors to queue
        for neighbor in self.get_neighbors(current):
            # Don't add blocked cells
            if self.map[current[1]][current[0]] == BLOCK_CHAR:
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
        if len(self.queue) == 0:
            return
        val = self.peek_queue()
        self.queue.remove(val)
        return val[0]

    def peek_queue(self):
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
        if len(self.queue) == 0:
            return
        self.path[:] = []
        current = self.peek_queue()[0]
        while current in self.previous:
            self.path.append(current)
            current = self.previous[current]

    def draw_board(self):
        for i in range(self.size):
            for k in range(self.size):
                left = k * CELL_SIZE + (k+1) * BORDER_WIDTH
                top = i * CELL_SIZE + (i+1) * BORDER_WIDTH
                rect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
                color = BG_COLOR
                if self.map[i][k] == BLOCK_CHAR:
                    color = BLOCK_COLOR
                elif self.map[i][k] == START_CHAR:
                    color = START_COLOR
                elif self.map[i][k] == END_CHAR:
                    color = END_COLOR
                elif (k, i) in self.path:
                    color = PATH_COLOR
                pygame.draw.rect(self.screen, color, rect)


if __name__ == '__main__':
    input = list(sys.stdin)
    AStarVisual(int(input[0]), input[1:])
