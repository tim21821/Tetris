# TODO: collide-Funktionen bauen für alle; check_tetris überarbeiten

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


def check_tetris(y, grid):
    for x in grid[:, y]:
        if x == None:
            return False
    return True


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

    def move_down(self):
        self.y += 1


class Shape:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1


class O(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "yellow"
        self.height = 2
        self.width = 2

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x, self.y - 1] = Block(self.x, self.y - 1, self.color)
        grid[self.x - 1, self.y] = Block(self.x - 1, self.y, self.color)
        grid[self.x, self.y] = Block(self.x, self.y, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x, self.y - 1] = None
        grid[self.x - 1, self.y] = None
        grid[self.x, self.y] = None
        return grid

    def collide(self, grid):
        if (grid[self.x - 1, self.y + 1] != None) or (grid[self.x, self.y + 1] != None):
            return True
        return False


class I(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "blue"
        self.height = 4
        self.width = 1

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x - 1, self.y] = Block(self.x - 1, self.y, self.color)
        grid[self.x - 1, self.y + 1] = Block(self.x - 1, self.y + 1, self.color)
        grid[self.x - 1, self.y + 2] = Block(self.x - 1, self.y + 2, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x - 1, self.y] = None
        grid[self.x - 1, self.y + 1] = None
        grid[self.x - 1, self.y + 2] = None
        return grid


class T(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "magenta"
        self.height = 2

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x, self.y - 1] = Block(self.x, self.y - 1, self.color)
        grid[self.x + 1, self.y - 1] = Block(self.x + 1, self.y - 1, self.color)
        grid[self.x, self.y] = Block(self.x, self.y, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x, self.y - 1] = None
        grid[self.x + 1, self.y - 1] = None
        grid[self.x, self.y] = None
        return grid


class Z(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "green"
        self.height = 2

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x, self.y - 1] = Block(self.x, self.y - 1, self.color)
        grid[self.x, self.y] = Block(self.x, self.y, self.color)
        grid[self.x + 1, self.y] = Block(self.x + 1, self.y, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x, self.y - 1] = None
        grid[self.x, self.y] = None
        grid[self.x + 1, self.y] = None
        return grid


class S(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "red"
        self.height = 2

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x, self.y - 1] = Block(self.x, self.y - 1, self.color)
        grid[self.x - 1, self.y] = Block(self.x - 1, self.y, self.color)
        grid[self.x - 2, self.y] = Block(self.x - 2, self.y, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x, self.y - 1] = None
        grid[self.x - 1, self.y] = None
        grid[self.x - 2, self.y] = None
        return grid


class L(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "orange"
        self.height = 3

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x - 1, self.y] = Block(self.x - 1, self.y, self.color)
        grid[self.x - 1, self.y + 1] = Block(self.x - 1, self.y + 1, self.color)
        grid[self.x, self.y + 1] = Block(self.x, self.y + 1, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x - 1, self.y] = None
        grid[self.x - 1, self.y + 1] = None
        grid[self.x, self.y + 1] = None
        return grid


class J(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "pink"
        self.height = 3

    def make(self, grid):
        grid[self.x - 1, self.y - 1] = Block(self.x - 1, self.y - 1, self.color)
        grid[self.x - 1, self.y] = Block(self.x - 1, self.y, self.color)
        grid[self.x - 1, self.y + 1] = Block(self.x - 1, self.y + 1, self.color)
        grid[self.x - 2, self.y + 1] = Block(self.x - 2, self.y + 1, self.color)
        return grid

    def destroy(self, grid):
        grid[self.x - 1, self.y - 1] = None
        grid[self.x - 1, self.y] = None
        grid[self.x - 1, self.y + 1] = None
        grid[self.x - 2, self.y + 1] = None
        return grid


def main():
    run = True
    draw_grid(WIN)
    test_block = Block(3, 1, "pink")
    test_block.draw(WIN)
    test_block2 = Block(4, 1, "green")
    test_block2.draw(WIN)
    pygame.display.flip()
    grid = np.full((X_SIZE, Y_SIZE + 4), None)
    shapes = [O, I, T, Z, S, L, J]
    queue = []
    points = 0
    moving = False
    while run:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        if len(queue) == 0:
            queue = random.sample(shapes, len(shapes))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and current.x > 1:
            grid = current.destroy(grid)
            current.move_left()
            grid = current.make(grid)
        if keys[pygame.K_RIGHT] and current.x < X_SIZE - current.width + 1:
            grid = current.destroy(grid)
            current.move_right()
            grid = current.make(grid)

        if (
            moving
            and current.y <= Y_SIZE + 4 - current.height
            and not current.collide(grid)
        ):
            grid = current.destroy(grid)
            current.move_down()
            grid = current.make(grid)
        else:
            # current = queue.pop(0)(4, 1)
            current = O(4, 1)
            grid = current.make(grid)
            moving = True

        if current.y <= 4 - current.height:
            if current.collide(grid):
                print("Verloren!")
                run = False

        for y in range(Y_SIZE):
            if check_tetris(y, grid):
                points += 10
                print(points)
                for x in grid[:, y]:
                    x = None
                for i in range(y + 1, Y_SIZE):
                    for j, x in enumerate(grid[:, i]):
                        x.y -= 1
                        grid[j, i - 1] = x
                        grid[j, i] = None

        WIN.fill("white")
        draw_grid(WIN)
        for x in grid:
            for y in x:
                if not y == None:
                    y.draw(WIN)
        pygame.display.flip()


if __name__ == "__main__":
    main()