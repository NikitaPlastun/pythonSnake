import pygame
import sys
import random
import pygame_menu
pygame.init()

bg_menu_color = (154, 205, 50)
size_block = 20
frame_color = (154, 205, 50)
white = (255, 255, 255)
blue = (177, 180, 250)
red = (224, 0, 0)
header_color = (82, 115, 76)
snake_color = (19, 21, 87)
count_blocks = 20
header_margin = 70
margin = 1
size = [size_block * count_blocks + 2 * size_block + margin + count_blocks,
        size_block * count_blocks + 2 * size_block + margin + count_blocks + header_margin]

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)

class snakeblock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def is_inside (self):
        return 0<= self.x < count_blocks and 0<= self.y <count_blocks

    def __eq__(self, other):
        return isinstance(other, snakeblock) and self.x == other.x and self.y == other.y

def draw_block(color,row,column):
    pygame.draw.rect(screen, color, [size_block + column * size_block + margin * (column + 1),
                                     header_margin + size_block + row * size_block + margin * (row + 1),
                                     size_block, size_block])

def start_the_game():

    def get_random_empty_block():
        x = random.randint(0, count_blocks - 1)
        y = random.randint(0, count_blocks - 1)
        empty_block = snakeblock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, count_blocks - 1)
            empty_block.y = random.randint(0, count_blocks - 1)
        return empty_block

    snake_blocks = [snakeblock(9, 8), snakeblock(9, 9), snakeblock(9, 10)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exit")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col !=0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col !=0:
                    buf_row = 1
                    buf_col = 0

                elif event.key == pygame.K_LEFT and d_row !=0:
                    buf_row = 0
                    buf_col = -1

                elif event.key == pygame.K_RIGHT and d_row !=0:
                    buf_row = 0
                    buf_col = 1

        screen.fill(frame_color)
        pygame.draw.rect(screen, header_color, [0, 0,size[0],header_margin])

        text_total = courier.render(f"Total: {total}", bool(0), white)
        text_speed = courier.render(f"Speed: {speed}", bool(0), white)
        screen.blit(text_total, (size_block, size_block))
        screen.blit(text_speed, (size_block+230, size_block))

        for row in range(count_blocks):
            for column in range(count_blocks):
                if (row + column) % 2 == 0:
                    color = blue
                else:
                    color = white

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            print("Game Over")
            break
            # pygame.quit()
            # sys.exit()

        draw_block(red, apple.x, apple.y)

        for block in snake_blocks:
            draw_block(snake_color, block.x, block.y)

        pygame.display.flip()
        if apple == head:
            total +=1
            speed = total//5 + 1
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        d_row = buf_row
        d_col = buf_col

        new_head = snakeblock(head.x +d_row, head.y + d_col)

        if new_head in snake_blocks:
            print("Game Over")
            break
            # pygame.quit()
            # sys.exit()

        snake_blocks.append(new_head)
        snake_blocks.pop(0)


        timer.tick(3+speed)

main_theme=pygame_menu.themes.THEME_DARK.copy()
main_theme.set_background_color_opacity(0.6)
menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=main_theme)

menu.add.text_input('Player name :', default='Player 1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


while True:

    screen.fill(bg_menu_color)

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()
# :)