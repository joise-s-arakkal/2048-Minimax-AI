import pygame
import random
import copy

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 500
SIZE = 4
TILE_SIZE = WIDTH // SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 with Minimax AI")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Colors for UI
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
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
    2048: (237, 194, 46),
}
TEXT_COLOR = BLACK

# Font
font = pygame.font.SysFont("Arial", 24, bold=True)
font_big = pygame.font.SysFont("Arial", 40, bold=True)

# Initialize board
def init_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    add_tile(board)
    add_tile(board)
    return board

def add_tile(board):
    empty_tiles = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if empty_tiles:
        r, c = random.choice(empty_tiles)
        board[r][c] = 2 if random.random() < 0.9 else 4

# Move the board in four directions
def move_left(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for r in range(SIZE):
        fill_pos = 0
        for c in range(SIZE):
            if board[r][c] != 0:
                if new_board[r][fill_pos] == 0:
                    new_board[r][fill_pos] = board[r][c]
                elif new_board[r][fill_pos] == board[r][c]:
                    new_board[r][fill_pos] *= 2
                    fill_pos += 1
                else:
                    fill_pos += 1
                    new_board[r][fill_pos] = board[r][c]
    return new_board

def rotate_board(board):
    return [[board[c][r] for c in range(SIZE)] for r in range(SIZE - 1, -1, -1)]

def move(board, direction):
    if direction == 0:  # Left
        return move_left(board)
    elif direction == 1:  # Up
        return rotate_board(rotate_board(rotate_board(move_left(rotate_board(board)))))
    elif direction == 2:  # Right
        return rotate_board(rotate_board(move_left(rotate_board(rotate_board(board)))))
    elif direction == 3:  # Down
        return rotate_board(move_left(rotate_board(rotate_board(rotate_board(board)))))

def is_move_possible(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                return True
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                return True
    return False

# Minimax AI with alpha-beta pruning
def alpha_beta(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or not is_move_possible(board):
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move_dir in range(4):
            new_board = move(board, move_dir)
            if new_board != board:
                add_tile(new_board)
                eval = alpha_beta(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for move_dir in range(4):
            new_board = move(board, move_dir)
            if new_board != board:
                eval = alpha_beta(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def best_move(board, depth=3):
    best_score = -float('inf')
    best_move = None
    for move_dir in range(4):
        new_board = move(board, move_dir)
        if new_board != board:
            add_tile(new_board)
            score = alpha_beta(new_board, depth - 1, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = move_dir
    return best_move

# Heuristic for board evaluation
def evaluate_board(board):
    return (0.1 * count_empty_tiles(board) +
            1.0 * tile_merging_potential(board) +
            1.5 * monotonicity(board) +
            0.5 * max_tile_in_corner(board) +
            0.8 * weighted_grid_score(board))

# Count empty tiles
def count_empty_tiles(board):
    return sum(1 for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0)

# Tile merging potential heuristic
def tile_merging_potential(board):
    score = 0
    for r in range(SIZE):
        for c in range(SIZE):
            if c < SIZE - 1 and board[r][c] == board[r][c + 1]:
                score += board[r][c]
            if r < SIZE - 1 and board[r][c] == board[r + 1][c]:
                score += board[r][c]
    return score

# Monotonicity heuristic
def monotonicity(board):
    score = 0
    for r in range(SIZE):
        for c in range(SIZE - 1):
            if board[r][c] >= board[r][c + 1]:
                score += board[r][c]
            else:
                score -= board[r][c]
    for c in range(SIZE):
        for r in range(SIZE - 1):
            if board[r][c] >= board[r + 1][c]:
                score += board[r][c]
            else:
                score -= board[r][c]
    return score

# Max tile in a corner heuristic
def max_tile_in_corner(board):
    max_tile = max(max(row) for row in board)
    if board[0][0] == max_tile or board[0][SIZE-1] == max_tile or board[SIZE-1][0] == max_tile or board[SIZE-1][SIZE-1] == max_tile:
        return max_tile
    return 0

# Weighted grid for tile placement
def weighted_grid_score(board):
    weighted_grid = [
        [15, 13, 9, 5],
        [13, 9, 5, 3],
        [9, 5, 3, 1],
        [5, 3, 1, 0]
    ]
    score = 0
    for r in range(SIZE):
        for c in range(SIZE):
            score += board[r][c] * weighted_grid[r][c]
    return score

# Draw the board
def draw_board(board, score, game_over=False):
    screen.fill(BACKGROUND_COLOR)  # Set background color
    
    # Draw each tile
    for r in range(SIZE):
        for c in range(SIZE):
            tile_value = board[r][c]
            rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE)
            
            # Set the tile background color
            color = CELL_COLORS.get(tile_value, (205, 193, 180))  # Default for tiles > 2048
            pygame.draw.rect(screen, color, rect)
            
            if tile_value != 0:
                label = font_big.render(str(tile_value), True, TEXT_COLOR)
                text_rect = label.get_rect(center=(c * TILE_SIZE + TILE_SIZE // 2, r * TILE_SIZE + 100 + TILE_SIZE // 2))
                screen.blit(label, text_rect)

    # Draw the score
    label = font.render(f"Score: {round(score,2)}", True, TEXT_COLOR)
    screen.blit(label, (10, 10))

    if game_over:
        game_over_label = font_big.render("Game Over!", True, TEXT_COLOR)
        screen.blit(game_over_label, (WIDTH // 2 - game_over_label.get_width() // 2, 70 - game_over_label.get_height() // 2))
        retry_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50)
        pygame.draw.rect(screen, RED, retry_button)
        retry_label = font.render("Retry", True, WHITE)
        screen.blit(retry_label, (WIDTH // 2 - retry_label.get_width() // 2, HEIGHT // 2 + 30 + (50 - retry_label.get_height()) // 2))

def main():
    board = init_board()
    clock = pygame.time.Clock()
    running = True
    score = 0
    game_over = False

    while running:
        draw_board(board, score, game_over)
        pygame.display.update()

        new_board = copy.deepcopy(board)
        move_made = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = pygame.mouse.get_pos()
                retry_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
                if retry_button.collidepoint(mouse_pos):
                    board = init_board()
                    score = 0
                    game_over = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                new_board = move(board, 0)
                move_made = (new_board != board)
            elif keys[pygame.K_UP]:
                new_board = move(board, 1)
                move_made = (new_board != board)
            elif keys[pygame.K_RIGHT]:
                new_board = move(board, 2)
                move_made = (new_board != board)
            elif keys[pygame.K_DOWN]:
                new_board = move(board, 3)
                move_made = (new_board != board)
            elif keys[pygame.K_a]:  # Press 'A' to activate AI
                ai_move = best_move(board)
                if ai_move is not None:
                    new_board = move(board, ai_move)
                    move_made = (new_board != board)

            if move_made:
                add_tile(new_board)
                score += evaluate_board(new_board) - evaluate_board(board)
                board = new_board

            if not is_move_possible(board):
                game_over = True

        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
