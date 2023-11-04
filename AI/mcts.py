import pygame
import random
import copy
import time

# Define some constants for the game
GRID_SIZE = 4
TILE_SIZE = 100
WINDOW_SIZE = TILE_SIZE * GRID_SIZE
BG_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# utility functions

def get_direction_text(direction):
    return "up" if direction == 0 else "right" if direction == 1 else "down" if direction == 2 else "left" if direction == 3 else direction


class Game:
    def __init__(self, gui=True, grid=None):
        # the gui flag is used to determine whether to render the game or not (might be useful for testing)
        # Initialize the game
        if gui:
            self.gui = True
            pygame.init()
            self.window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
            self.font = pygame.font.SysFont("Arial", 32)
        if not gui:
            self.gui = False
        self.score = 0
        if grid:
            self.grid = grid
        else:
            self.reset()

    def reset(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.add_random_tile()
        self.add_random_tile()
        self.score = 0

    def add_random_tile(self):
        # Add a random tile to the grid, probability of adding a 2 is 90% and 4 is 10%
        empty_tiles = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    empty_tiles.append((i, j))
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def render(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # draw the tile
                pygame.draw.rect(self.window, TILE_COLORS[self.grid[i][j]], (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                # add the text to the tile
                text = self.font.render(str(self.grid[i][j]) if self.grid[i][j] else "", True, (119, 110, 101))
                text_rect = text.get_rect()
                text_rect.center = (j * TILE_SIZE + TILE_SIZE / 2, i * TILE_SIZE + TILE_SIZE / 2)
                self.window.blit(text, text_rect)

                # add a border around the tiles
                pygame.draw.rect(self.window, (187, 173, 160), (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE), 5)

        pygame.display.update()

    def move(self, direction):
        # direction: 0 - up, 1 - right, 2 - down, 3 - left
        # slide the tiles in the given direction
        merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        initial_grid = [row[:] for row in self.grid]

        # Slide tiles as far as possible in the given direction, merging tiles of the same value once.
        if direction == 0:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    shift = 0
                    for k in range(i): # k checks all tiles between i and 0
                        if self.grid[k][j] == 0:
                            shift += 1
                    
                    if shift:
                        self.grid[i - shift][j] = self.grid[i][j]
                        self.grid[i][j] = 0

                    if i - shift - 1 >= 0 and self.grid[i - shift - 1][j] == self.grid[i - shift][j] and not merged[i - shift - 1][j] and not merged[i - shift][j]:
                        self.score += self.grid[i - shift][j] * 2
                        self.grid[i - shift - 1][j] *= 2
                        self.grid[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

        elif direction == 1:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE - 1, -1, -1):
                    shift = 0
                    for k in range(j + 1, GRID_SIZE):
                        if self.grid[i][k] == 0:
                            shift += 1

                    if shift:
                        self.grid[i][j + shift] = self.grid[i][j]
                        self.grid[i][j] = 0

                    if j + shift + 1 < GRID_SIZE and self.grid[i][j + shift + 1] == self.grid[i][j + shift] and not merged[i][j + shift + 1] and not merged[i][j + shift]:
                        self.score += self.grid[i][j + shift] * 2
                        self.grid[i][j + shift + 1] *= 2
                        self.grid[i][j + shift] = 0
                        merged[i][j + shift + 1] = True

        elif direction == 2:
            for i in range(GRID_SIZE - 1, -1, -1):
                for j in range(GRID_SIZE):
                    shift = 0
                    for k in range(i + 1, GRID_SIZE):
                        if self.grid[k][j] == 0:
                            shift += 1

                    if shift:
                        self.grid[i + shift][j] = self.grid[i][j]
                        self.grid[i][j] = 0

                    if i + shift + 1 < GRID_SIZE and self.grid[i + shift + 1][j] == self.grid[i + shift][j] and not merged[i + shift + 1][j] and not merged[i + shift][j]:
                        self.score += self.grid[i + shift][j] * 2
                        self.grid[i + shift + 1][j] *= 2
                        self.grid[i + shift][j] = 0
                        merged[i + shift + 1][j] = True

        elif direction == 3:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    shift = 0
                    for k in range(j):
                        if self.grid[i][k] == 0:
                            shift += 1

                    if shift:
                        self.grid[i][j - shift] = self.grid[i][j]
                        self.grid[i][j] = 0

                    if j - shift - 1 >= 0 and self.grid[i][j - shift - 1] == self.grid[i][j - shift] and not merged[i][j - shift - 1] and not merged[i][j - shift]:
                        self.score += self.grid[i][j - shift] * 2
                        self.grid[i][j - shift - 1] *= 2
                        self.grid[i][j - shift] = 0
                        merged[i][j - shift - 1] = True

        if self.grid != initial_grid:
            self.add_random_tile()
            if self.check_game_over():
                if self.gui:
                    pygame.time.delay(5000)
                    pygame.quit()
                return (1, self.grid)
            if self.gui:
                self.render()
            return (0, self.grid)
        else:
            return (2, self.grid)

    def check_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return
                if i > 0 and self.grid[i - 1][j] == self.grid[i][j]:
                    return
                if i < GRID_SIZE - 1 and self.grid[i + 1][j] == self.grid[i][j]:
                    return
                if j > 0 and self.grid[i][j - 1] == self.grid[i][j]:
                    return
                if j < GRID_SIZE - 1 and self.grid[i][j + 1] == self.grid[i][j]:
                    return

        # overlay text on the screen
        if self.gui:
            text = self.font.render("Game Over!", True, (119, 110, 101))
            text_rect = text.get_rect()
            text_rect.center = (WINDOW_SIZE / 2, WINDOW_SIZE / 2)
            self.window.blit(text, text_rect)
            pygame.display.update()
        return True
        

    def __str__(self):
        return "\n".join([" ".join([str(self.grid[i][j]) for j in range(GRID_SIZE)]) for i in range(GRID_SIZE)])
    
# def random_policy(game):
#     game_copy = copy.deepcopy(game)
#     while not game_copy.check_game_over():
#         game_copy.move(random.randint(0, 3))
#     return game_copy.score, max(max(row) for row in game_copy.grid)

def monotonicity(game):
    monotonicity = 0
    for i in range(4):
        for j in range(4):
            if i == 0 and j == 0:
                continue
            if i == 0:
                monotonicity += game.grid[i][j] - game.grid[i][j - 1]
            elif j == 0:
                monotonicity += game.grid[i][j] - game.grid[i - 1][j]
            else:
                monotonicity += abs(game.grid[i][j] - game.grid[i - 1][j]) + abs(game.grid[i][j] - game.grid[i][j - 1])
    return monotonicity

def monotonicity(game):
    monotonicity = 0
    for i in range(4):
        for j in range(4):
            if i == 0 and j == 0:
                continue
            if i == 0:
                monotonicity += game.grid[i][j] - game.grid[i][j - 1]
            elif j == 0:
                monotonicity += game.grid[i][j] - game.grid[i - 1][j]
            else:
                monotonicity += abs(game.grid[i][j] - game.grid[i - 1][j]) + abs(game.grid[i][j] - game.grid[i][j - 1])
    return monotonicity

def random_policy(game):
    game_copy = copy.deepcopy(game)
    status = True
    while not game_copy.check_game_over():
        max_tile = 0
        if status:
            max_tile = max(max(row) for row in game_copy.grid)

        if max_tile < 512:
            game_copy.move(random.randint(0, 3))
        else:
            status = False
        
        if not status:
            mono_decisions = []
            for i in range(4):
                game_copy_temp = copy.deepcopy(game_copy)
                result, grid = game_copy_temp.move(i)
                monotonicity_score = monotonicity(game_copy_temp)
                mono_decisions.append({"move": i, "monotonicity": monotonicity_score})
            
            best_move = max(mono_decisions, key=lambda x: x["monotonicity"])["move"]
            game_copy.move(best_move)

    return game_copy.score, max(max(row) for row in game_copy.grid)

def mcts(initial_game):
    # urdl_score_max_tile = [0, 0, 0, 0]
    urdl_score = [0, 0, 0, 0]

    for move in range(4):
        game_copy = copy.deepcopy(initial_game)
        result, grid = game_copy.move(move)

        if result == 2:
            continue

        # try random policy for 100 games
        for i in range(81):
            output = random_policy(game_copy)

            urdl_score[move] += output[0]
    
    print(urdl_score)

    best_move_by_score = urdl_score.index(max(urdl_score))

    initial_game.move(best_move_by_score)
    print(str(initial_game))
    print("Score: " + str(initial_game.score))
    print()

def monte_carlo_simulation(initial_game):
    game = copy.deepcopy(initial_game)
    iterations = 1
    while not game.check_game_over():
        mcts(game)
        iterations += 1

    print("Final State:\n", str(game))
    print("Score: " + str(game.score))
    print("Max Tile: " + str(max(max(row) for row in game.grid)))

    return game.score, max(max(row) for row in game.grid), game.grid
    

Sum = 0
Max = 0
Max_game = None
_2prob = 0
_4prob = 0
_8prob = 0
_16prob = 0
_32prob = 0
_64prob = 0
_128prob = 0
_256prob = 0
_512prob = 0
_1024prob = 0
_2048prob = 0
_4096prob = 0

init_time = time.time()
for i in range(1):
    game = Game(gui=False)
    (score, max_tile, grid) = monte_carlo_simulation(game)
    Sum += score
    if score > Max:
        Max = score
        Max_game = grid
    if any(4096 in row for row in grid):
        _4096prob += 1
    if any(2048 in row for row in grid):
        _2048prob += 1
    if any(1024 in row for row in grid):
        _1024prob += 1
    if any(512 in row for row in grid):
        _512prob += 1
    if any(256 in row for row in grid):
        _256prob += 1
    if any(128 in row for row in grid):
        _128prob += 1
    if any(64 in row for row in grid):
        _64prob += 1
    if any(32 in row for row in grid):
        _32prob += 1
    if any(16 in row for row in grid):
        _16prob += 1
    if any(8 in row for row in grid):
        _8prob += 1
    if any(4 in row for row in grid):
        _4prob += 1
    if any(2 in row for row in grid):
        _2prob += 1

print("\nTime taken (s): " + str(time.time() - init_time))

print("\ncAverage Score: " + str(Sum / 100))
print("Max Score: " + str(Max))
print("Best Game:\n", str(Max_game))
print("2: " + str(_2prob/100))
print("4: " + str(_4prob/100))
print("8: " + str(_8prob/100))
print("16: " + str(_16prob/100))
print("32: " + str(_32prob/100))
print("64: " + str(_64prob/100))
print("128: " + str(_128prob/100))
print("256: " + str(_256prob/100))
print("512: " + str(_512prob/100))
print("1024: " + str(_1024prob/100))
print("2048: " + str(_2048prob/100))
print("4096: " + str(_4096prob/100))