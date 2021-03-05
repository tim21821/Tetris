import pygame
import numpy as np
import random


BLOCK_SIZE = 40
X_SIZE = 10
Y_SIZE = 20
pygame.init()
WIN = pygame.display.set_mode((BLOCK_SIZE * X_SIZE, BLOCK_SIZE * Y_SIZE))
WIN.fill("white")
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()


def check_tetris(grid, y):
    for x in grid[y]:
        if x == None:
            return False
    return True


def delete_line(grid, y):
    for i in range(0, y):
        grid[y - i] = grid[y - i - 1]
        for block in grid[y - i]:
            if block != None:
                block.y = y - i
    grid[0] = np.full(X_SIZE, None)
    return grid


def draw_grid(window):
    for x in range(10):
        for y in range(20):
            pygame.draw.rect(
                window,
                "black",
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                width=1,
            )


class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.current = True

    def draw(self, window):
        if self.y >= 4:
            pygame.draw.rect(
                window,
                self.color,
                (
                    self.x * BLOCK_SIZE + 1,
                    (self.y - 4) * BLOCK_SIZE + 1,
                    BLOCK_SIZE - 2,
                    BLOCK_SIZE - 2,
                ),
            )


class Shape:
    offsets = {
        "O": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
        "I": [
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(-1, 1), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
            [(-1, 2), (0, 2), (1, 2), (2, 2)],
        ],
        "T": [
            [(0, 0), (-1, 1), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (0, 2)],
            [(0, 2), (-1, 1), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (-1, 1), (0, 2)],
        ],
        "Z": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (1, 1), (0, 1), (0, 2)],
        ],
        "S": [
            [(1, 0), (2, 0), (1, 1), (0, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (1, 2), (0, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "L": [
            [(2, 0), (2, 1), (1, 1), (0, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
        "J": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (1, 2), (0, 2)],
        ],
    }

    colors = {
        "O": "yellow",
        "I": "cyan",
        "T": "violet",
        "Z": "red",
        "S": "green",
        "L": "orange",
        "J": "blue",
    }

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.rotation = 0
        self.type = shape
        self.color = self.colors[self.type]

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def rotate(self):
        self.rotation += 1
        self.rotation %= len(self.offsets[self.type])

    def collide(self, grid, move_x, move_y):
        collision = False
        for i in range(4):
            x = self.x - 1 + self.offsets[self.type][self.rotation][i][0] + move_x
            y = self.y - 1 + self.offsets[self.type][self.rotation][i][1] + move_y
            if x < 0:
                collision = True
            elif x >= X_SIZE:
                collision = True
            elif y == Y_SIZE + 4:
                collision = True
            elif grid[y, x] != None:
                if not grid[y, x].current:
                    collision = True
        return collision

    def rot_collide(self, grid):
        collision = False
        for i in range(4):
            x = (
                self.x
                - 1
                + self.offsets[self.type][
                    (self.rotation + 1) % len(self.offsets[self.type])
                ][i][0]
            )
            y = (
                self.y
                - 1
                + self.offsets[self.type][
                    (self.rotation + 1) % len(self.offsets[self.type])
                ][i][1]
            )
            if x < 0:
                collision = True
            elif x >= X_SIZE:
                collision = True
            elif y == Y_SIZE + 4:
                collision = True
            elif grid[y, x] != None:
                if not grid[y, x].current:
                    collision = True
        return collision

    def make(self, grid):
        for i in range(4):
            x = self.x - 1 + self.offsets[self.type][self.rotation][i][0]
            y = self.y - 1 + self.offsets[self.type][self.rotation][i][1]
            grid[y, x] = Block(x, y, self.color)
        return grid

    def destroy(self, grid):
        for i in range(4):
            x = self.x - 1 + self.offsets[self.type][self.rotation][i][0]
            y = self.y - 1 + self.offsets[self.type][self.rotation][i][1]
            grid[y, x] = None
        return grid


def main():
    run = True
    draw_grid(WIN)
    grid = np.full((Y_SIZE + 5, X_SIZE), None)
    shapes = ["O", "I", "T", "Z", "S", "L", "J"]
    queue = []
    score = 0
    moving = False
    fps = 25
    counter = 0
    while run:
        clock.tick(fps)
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Du hast {score} Punkte erreicht!")
                run = False

        if len(queue) == 0:
            queue = random.sample(shapes, len(shapes))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not current.collide(grid, -1, 0):
            grid = current.destroy(grid)
            current.move_left()
            grid = current.make(grid)
        if keys[pygame.K_RIGHT] and not current.collide(grid, 1, 0):
            grid = current.destroy(grid)
            current.move_right()
            grid = current.make(grid)
        if keys[pygame.K_UP] and not current.rot_collide(grid):
            grid = current.destroy(grid)
            current.rotate()
            grid = current.make(grid)
        if keys[pygame.K_DOWN] and not current.collide(grid, 0, 1):
            grid = current.destroy(grid)
            current.move_down()
            grid = current.make(grid)

        if moving and not current.collide(grid, 0, 1):
            if counter % 5 == 0:
                grid = current.destroy(grid)
                current.move_down()
                grid = current.make(grid)
        else:
            counter = 0
            for i in range(len(grid)):
                if check_tetris(grid, i):
                    counter += 1
                    grid = delete_line(grid, i)
            if counter == 1:
                score += 40
            elif counter == 2:
                score += 100
            elif counter == 3:
                score += 300
            elif counter == 4:
                score += 1200

            for y in grid:
                for x in y:
                    if x != None:
                        x.current = False

            current = Shape(4, 1, queue.pop(0))
            if current.collide(grid, 0, 0):
                print(f"Gameover!\n Du hast {score} Punkte!")
                run = False
            grid = current.make(grid)
            moving = True

        WIN.fill("white")
        draw_grid(WIN)
        for x in grid:
            for y in x:
                if not y == None:
                    y.draw(WIN)
        pygame.display.flip()


if __name__ == "__main__":
    main()