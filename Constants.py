#SCREEN
WIDTH = 700
HEIGHT = 900
WIDTH1 = WIDTH - 100
WIDTH2 = WIDTH // 2
HEIGHT1 = HEIGHT - 200
HEIGHT2 = HEIGHT - 300
ROWS, COLS = 5, 5
SQUARE_SIZE = 100
LINE_WIDTH = 2
PADDING = SQUARE_SIZE //5

FPS = 60

#COLORS
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 128, 0)
BOARD = (150,53,44)
SQR = (224, 100, 58)

#DQN
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 5000