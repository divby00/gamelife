#!/usr/bin/env python

'''
Python implementation of Conway's Game of Life.
-----------------------------------------------
Rules:
* Any live cell with fewer than two live neighbours dies, as if caused by under-population.
* Any live cell with two or three live neighbours lives on to the next generation.
* Any live cell with more than three live neighbours dies, as if by over-population.
* Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''
import argparse
import pygame
import numpy
import random


class ArgumentParser(object):

    def __init__(self):
        self._parser = argparse.ArgumentParser(description="Conway's game of life")
        self._parser.add_argument('-w', '--width', type=int, help='Screen width in cells')
        self._parser.add_argument('-e', '--height', type=int, help='Screen height in cells')
        self._parser.add_argument('-c', '--cells', type=int, help='Random cells at init')
        self._args = self._parser.parse_args()
        self._width = 60 if self._args.width is None else self._args.width
        self._height = 40 if self._args.height is None else self._args.height
        self._cells = 0 if self._args.cells is None else self._args.cells
        self._size = self._width, self._height

    @property
    def size(self):
        return self._size

    @property
    def cells(self):
        return self._cells


class GameOfLife(object):

    DEAD = 0
    ALIVE = 1
    TILE_HEIGHT = 20
    TILE_WIDTH = 20

    def __init__(self):
        self._generation = 0
        self._running = False
        self._display = None
        self._matrix = None
        self._updated_matrix = None
        self._size = (None, None)
        self._mouse_position = None
        self._start = False

    def init(self):
        parser = ArgumentParser()
        pygame.init()
        self._size = parser.size
        self._display = pygame.display.set_mode((self._size[0] * GameOfLife.TILE_WIDTH
                                                , self._size[1] * GameOfLife.TILE_HEIGHT)
                                                , pygame.HWSURFACE)
        if self._display is not None:
            pygame.display.set_caption("Conway's Game of Life")
            pygame.mouse.set_visible(False)
            self._running = True
            self._matrix = numpy.zeros((self._size[1], self._size[0]))
            self._add_random_cells(parser.cells)

    def quit(self):
        pygame.quit()

    def loop(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

            mouse_info = pygame.mouse.get_pressed()
            self._mouse_position = pygame.mouse.get_pos()
            x = self._mouse_position[0] / GameOfLife.TILE_WIDTH
            y = self._mouse_position[1] / GameOfLife.TILE_HEIGHT
            self._mouse_position = (y, x)

            if mouse_info[0]:

                if self._start:
                    self._matrix = numpy.zeros((self._size[1], self._size[0]))
                
                self._matrix[y][x] = 1
                self._start = False
                self._generation = 0

            if mouse_info[2]:
                self._start = True

            if self._start:
                self._logic()
                self._generation += 1
            self._render()

    def _logic(self):
        self._updated_matrix = numpy.zeros((self._size[1], self._size[0]))
        for row in xrange(0, self._size[1]):
            for column in xrange(0, self._size[0]):
                cell_status = self._get_cell_status((row, column))
                self._updated_matrix[row][column] = cell_status
        self._matrix = self._updated_matrix

    def _get_cell_status(self, coordinates):
        neighbours = self._get_neighbours(coordinates)
        alive_neighbours = numpy.sum(neighbours)
        cell_is_alive = self._matrix[coordinates[0]][coordinates[1]]

        if cell_is_alive == 1:
            status = GameOfLife.ALIVE
            if alive_neighbours < 2 or alive_neighbours > 3:
                status = GameOfLife.DEAD
        else:
            status = GameOfLife.DEAD
            if alive_neighbours == 3:
                status = GameOfLife.ALIVE

        return status

    def _add_random_cells(self, cells_to_add):
        for c in xrange(cells_to_add):
            row = random.randint(0, self._size[1] - 1)
            column = random.randint(0, self._size[0] - 1)
            self._matrix[row][column] = 1

    def _get_neighbours(self, (row, column)):
        row_limit = 0 if row < 1 else row - 1
        column_limit = 0 if column < 1 else column - 1
        temporal_array = numpy.copy(self._matrix)
        temporal_array[row][column] = 0
        neighbours = numpy.copy(temporal_array[row_limit:row + 2, column_limit:column + 2])
        return neighbours
                
    def _render(self):
        self._display.fill((0, 0, 0))
        for row in xrange(0, self._size[1]):
            for column in xrange(0, self._size[0]):
                if self._matrix[row][column] == 1:
                    pygame.draw.rect(self._display, (random.randint(0, 150) + 100, 30, 30)
                                    , (column * GameOfLife.TILE_WIDTH
                                    , row * GameOfLife.TILE_HEIGHT
                                    , GameOfLife.TILE_WIDTH - 1
                                    , GameOfLife.TILE_HEIGHT - 1))
        # Render mouse position
        pygame.draw.rect(self._display, (random.randint(0, 150) + 100, 200, 200)
                        , (self._mouse_position[1] * GameOfLife.TILE_WIDTH
                        , self._mouse_position[0] * GameOfLife.TILE_HEIGHT
                        , GameOfLife.TILE_WIDTH - 1
                        , GameOfLife.TILE_HEIGHT - 1))
        
        pygame.display.set_caption("Conway's Game of Life - Generation: " + str(self._generation))
        pygame.display.flip()


def main():
    app = GameOfLife()
    app.init()
    app.loop()
    app.quit()


if __name__ == '__main__':
    main()
