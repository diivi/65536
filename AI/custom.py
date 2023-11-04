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
        # game over after 1 move for testing
        # self.grid = [
        #     [2, 4, 8, 16],
        #     [32, 64, 128, 256],
        #     [512, 1024, 2048, 256],
        #     [2, 4, 8, 16]
        # ]
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
            # print("Game State after moving " + get_direction_text(direction) + ":")
            # print(str(self))
            # print("Score: " + str(self.score))
            # print()
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

def check_monotonicity(grid):
    mono_score = 0
    prev_value = -1
    inc_score = 0
    dec_score = 0

    def score_cell(cell_loc):
        nonlocal prev_value
        nonlocal inc_score
        nonlocal dec_score
        tile = grid[cell_loc[0]][cell_loc[1]]
        tile_value = tile
        inc_score += tile_value
        if tile_value <= prev_value or prev_value == -1:
            dec_score += tile_value
            if tile_value < prev_value:
                inc_score -= prev_value
        prev_value = tile_value

    for i in range(GRID_SIZE):
        prev_value = -1
        inc_score = 0
        dec_score = 0
        for j in range(GRID_SIZE):
            score_cell((i, j))
        mono_score += max(inc_score, dec_score)

    for j in range(GRID_SIZE):
        prev_value = -1
        inc_score = 0
        dec_score = 0
        for i in range(GRID_SIZE):
            score_cell((i, j))
        mono_score += max(inc_score, dec_score)

    available_cells = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                available_cells.append((i, j))
    empty_cell_weight = 8

    empty_score = len(available_cells) * empty_cell_weight

    score = mono_score + empty_score
    return score

def get_next_states(grid, depth, game_monotonicty):
    """
    Plans a few moves ahead and returns the worst-case scenario grid quality,
    and the probability of that occurring, for each move
    """
    results = [None for _ in range(4)]

    for direction in range(4):
        game_copy = Game(gui=False, grid=copy.deepcopy(grid))
        result, grid = game_copy.move(direction)

        if result == 2:
            continue

        # Spawn a 2 in all possible locations.
        result = {
            "heuristic": -1,
            "probability": 1,
            "loss": 0,
            "direction": direction
        }

        # get all available cells where a 2 can be spawned
        available_cells = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 0:
                    available_cells.append((i, j))

        for cell_loc in available_cells:
            # if there is space between this empty cell and the nearest tile that we have placed, we don't need to check this location. The worst case is when the new 2 is spawned next to the nearest tile, since we have less space to work with. Let's collect the worst case scenarios:
            has_adjacent_tile = False

            # check if there is a tile lrud
            if cell_loc[0] > 0 and grid[cell_loc[0] - 1][cell_loc[1]] != 0:
                has_adjacent_tile = True
            if cell_loc[0] < GRID_SIZE - 1 and grid[cell_loc[0] + 1][cell_loc[1]] != 0:
                has_adjacent_tile = True
            if cell_loc[1] > 0 and grid[cell_loc[0]][cell_loc[1] - 1] != 0:
                has_adjacent_tile = True
            if cell_loc[1] < GRID_SIZE - 1 and grid[cell_loc[0]][cell_loc[1] + 1] != 0:
                has_adjacent_tile = True

            if not has_adjacent_tile:
                continue

            # create a game duplicate and spawn a 2 in this location
            game_copy = Game(gui=False, grid=copy.deepcopy(grid))
            game_copy.grid[cell_loc[0]][cell_loc[1]] = 2

            curr_result = {
                "heuristic": -1,
                "probability": 1,
                "loss": 0,
                "direction": direction
            }
            if depth == 0:
                # calculate the heuristic for this grid
                heuristic = check_monotonicity(game_copy.grid)
                curr_result["heuristic"] = heuristic
                curr_result["probability"] = 1
                curr_result["loss"] = max(game_monotonicty - heuristic, 0)
            else:
                # get the next states for this grid
                next_states = get_next_states(game_copy.grid, depth - 1, game_monotonicty)
                best_state = choose_best_state(next_states, game_monotonicty)               

                curr_result["heuristic"] = best_state["heuristic"]
                curr_result["probability"] = best_state["probability"]
                curr_result["loss"] = best_state["loss"]

            # // Compare this grid quality to the grid quality for other tile spawn locations.
            # // Take the WORST quality since we have no control over where the tile spawns,
            # // so assume the worst case scenario.
            if result["heuristic"] == -1 or curr_result["heuristic"] < result["heuristic"]:
                result["heuristic"] = curr_result["heuristic"]
                result["probability"] = curr_result["probability"] / len(available_cells)
            elif curr_result["heuristic"] == result["heuristic"]:
                result["probability"] += curr_result["probability"] / len(available_cells)
                
        results[direction] = result

    return results

def choose_best_state(next_states, original_monotonicity):
    best_state = None
    for next_state in next_states:
        if not next_state:
            continue
        if not best_state or next_state["loss"] < best_state["loss"] or (next_state["loss"] == best_state["loss"] and next_state["heuristic"] > best_state["heuristic"]) or (next_state["loss"] == best_state["loss"] and next_state["heuristic"] == best_state["heuristic"] and next_state["probability"] > best_state["probability"]):
            best_state = next_state

    if not best_state:
        best_state = {
            "heuristic": -1,
            "probability": 1,
            "loss": -original_monotonicity,
            "direction": 0
        }

    return best_state

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
    print()
    print("Initial Game State:")
    print(str(game), end="\n\n")

    while not game.check_game_over():
        game_monotonicty = check_monotonicity(game.grid)
        print(game_monotonicty, end="\n\n")

        next_states = get_next_states(game.grid, 3, game_monotonicty)
        print(next_states, end="\n\n")
        best_state = choose_best_state(next_states, game_monotonicty)
        print(best_state, end="\n\n")
        print(get_direction_text(best_state["direction"]), end="\n\n")

        game.move(best_state["direction"])
        print(str(game), end="\n\n")

    
#     Sum += score
#     if score > Max:
#         Max = score
#         Max_game = grid
#     if any(4096 in row for row in grid):
#         _4096prob += 1
#     if any(2048 in row for row in grid):
#         _2048prob += 1
#     if any(1024 in row for row in grid):
#         _1024prob += 1
#     if any(512 in row for row in grid):
#         _512prob += 1
#     if any(256 in row for row in grid):
#         _256prob += 1
#     if any(128 in row for row in grid):
#         _128prob += 1
#     if any(64 in row for row in grid):
#         _64prob += 1
#     if any(32 in row for row in grid):
#         _32prob += 1
#     if any(16 in row for row in grid):
#         _16prob += 1
#     if any(8 in row for row in grid):
#         _8prob += 1
#     if any(4 in row for row in grid):
#         _4prob += 1
#     if any(2 in row for row in grid):
#         _2prob += 1

# print("Time taken (s): " + str(time.time() - init_time))

# print("Average Score: " + str(Sum / 100))
# print("Max Score: " + str(Max))
# print("Best Game:\n", str(Max_game))
# print("2: " + str(_2prob/100))
# print("4: " + str(_4prob/100))
# print("8: " + str(_8prob/100))
# print("16: " + str(_16prob/100))
# print("32: " + str(_32prob/100))
# print("64: " + str(_64prob/100))
# print("128: " + str(_128prob/100))
# print("256: " + str(_256prob/100))
# print("512: " + str(_512prob/100))
# print("1024: " + str(_1024prob/100))
# print("2048: " + str(_2048prob/100))
# print("4096: " + str(_4096prob/100))    