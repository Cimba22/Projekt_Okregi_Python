import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

block_size = 30
left_margin = 40
upper_margin = 50

size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Okręgi")

font_size = int(block_size//1.5)
font = pygame.font.SysFont('notosans', font_size)

def draw_grid():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    for y in range(11):
        for x in range(11):
            #Hor grid1
            pygame.draw.line(screen, BLACK, (left_margin, upper_margin+y*block_size),
                             (left_margin+10*block_size,upper_margin+y*block_size), 1)
            #Vert grid1
            pygame.draw.line(screen, BLACK, (left_margin+x*block_size, upper_margin),
                             (left_margin+x*block_size, upper_margin+10*block_size), 1)
            # Hor grid2
            pygame.draw.line(screen, BLACK, (left_margin+15*block_size, upper_margin + y * block_size),
                             (left_margin + 25 * block_size, upper_margin + y * block_size), 1)
            # Vert grid2
            pygame.draw.line(screen, BLACK, (left_margin + x * block_size+15*block_size, upper_margin),
                             (left_margin + x * block_size+15*block_size, upper_margin + 10 * block_size), 1)

            if y < 10:
                num_vert = font.render(str(y+1), True, BLACK)
                letters_hor = font.render(letters[y], True, BLACK)

                num_vert_width = num_vert.get_width()
                num_vert_height = num_vert.get_height()
                letters_hor_width = letters_hor.get_width()

                #Vert num grid1
                screen.blit(num_vert, (left_margin - (block_size//2+num_vert_width//2), upper_margin + y*block_size+ (block_size//2 - num_vert_height//2)))
                #Hor letters grid1
                screen.blit(letters_hor, (left_margin + y*block_size + (block_size//2 - letters_hor_width//2), upper_margin + 10 *block_size))

                # Vert num grid2
                screen.blit(num_vert, (left_margin - (block_size // 2 + num_vert_width // 2) +15 *block_size,
                                       upper_margin + y * block_size + (block_size // 2 - num_vert_height // 2)))
                # Hor letters grid2
                screen.blit(letters_hor, (left_margin + y * block_size + (block_size // 2 - letters_hor_width // 2) + 15*block_size,
                                          upper_margin + 10 * block_size))

def main():
    game_over = False
    screen.fill(WHITE)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        draw_grid()
        pygame.display.update()

main()
pygame.quit()