import pygame
import sys
import random
import time

# Inisialisasi Pygame
pygame.init()

# Konstanta
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Membuat jendela game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Papan permainan
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fungsi untuk menggambar garis-garis pada papan
def draw_lines():
    # Garis horizontal
    pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Garis vertikal
    pygame.draw.line(screen, BLACK, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Fungsi untuk menggambar simbol X dan O pada papan
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "X":
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, BLUE,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

# Fungsi untuk menandai kotak yang dipilih oleh pemain
def mark_square(row, col, player):
    board[row][col] = player

# Fungsi untuk memeriksa apakah ada pemenang atau permainan seri
def check_winner():
    # Cek baris dan kolom
    for i in range(BOARD_ROWS):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i], [(0, i), (1, i), (2, i)]
    # Cek diagonal
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2], [(0, 2), (1, 1), (2, 0)]
    # Cek apakah permainan seri
    if all(board[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS)):
        return "Tie", []
    return None, []

# Fungsi untuk mengevaluasi skor
def evaluate():
    winner, _ = check_winner()
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    else:
        return 0

# Fungsi Minimax
def minimax(depth, is_maximizing):
    if depth == 0 or check_winner()[0]:
        return evaluate()

    if is_maximizing:
        best_score = -float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(depth - 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(depth - 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

# Fungsi untuk melakukan langkah komputer
def computer_move():
    best_score = -float("inf")
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == " ":
                board[row][col] = "X"
                score = minimax(3, False)
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# Fungsi untuk menampilkan pesan peringatan pada akhir permainan
def display_result(result):
    font = pygame.font.Font(None, 40)
    text = font.render(result, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

# Fungsi untuk menampilkan pesan pilihan restart atau keluar
def display_option(option):
    font = pygame.font.Font(None, 30)
    text = font.render(option, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(text, text_rect)

# Fungsi utama game
def main():
    running = True
    player = "O"
    game_over = False
    option_displayed = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            if player == "O":
                mouseX, mouseY = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE

                    if board[clicked_row][clicked_col] == " ":
                        mark_square(clicked_row, clicked_col, player)
                        player = "X"
                        if check_winner()[0]:
                            game_over = True
            else:
                time.sleep(2)  # Jeda 2 detik sebelum komputer memilih kotak
                move = computer_move()
                if move:
                    mark_square(move[0], move[1], "X")
                    player = "O"
                    if check_winner()[0]:
                        game_over = True

        screen.fill(WHITE)
        draw_lines()
        draw_figures()

        result = check_winner()
        if result[0]:
            game_over = True
            if result[0] == "Tie":
                display_result("It's a Tie!")
            else:
                display_result(f"{result[0]} Wins!")
            if not option_displayed:
                display_option("Press R to Restart or Q to Quit")
                option_displayed = True

        # Handle restart or quit option
        keys = pygame.key.get_pressed()
        if option_displayed:
            if keys[pygame.K_r]:
                # Reset game
                board.clear()
                board.extend([[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)])
                game_over = False
                option_displayed = False
            elif keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()
