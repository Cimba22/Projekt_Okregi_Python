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

font_size = int(block_size/1.5)
font = pygame.font.SysFont('notosans', font_size)

class ShipsOnGrid:
    def __init__(self):
        self.available_blocks = set((a, b) for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    def create_ship(self, number_of_blocks, avaibable_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(avaibable_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.add_block_to_ship(x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.add_block_to_ship(y, str_rev, x_or_y, ship_coordinates)
        if self.if_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, avaibable_blocks)

    def add_block_to_ship(self, coor, str_rev, x_or_y, ship_coordinates):

        if(coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev


    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)



def draw_grid():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    for i in range(11):

        #Hor grid1
        pygame.draw.line(screen, BLACK, (left_margin, upper_margin+i*block_size),
                         (left_margin+10*block_size,upper_margin+i*block_size), 1)
        #Vert grid1
        pygame.draw.line(screen, BLACK, (left_margin+i*block_size, upper_margin),
                         (left_margin+i*block_size, upper_margin+10*block_size), 1)
        # Hor grid2
        pygame.draw.line(screen, BLACK, (left_margin+15*block_size, upper_margin + i * block_size),
                         (left_margin + 25 * block_size, upper_margin + i * block_size), 1)
        # Vert grid2
        pygame.draw.line(screen, BLACK, (left_margin + i * block_size+15*block_size, upper_margin),
                         (left_margin + i * block_size+15*block_size, upper_margin + 10 * block_size), 1)

        if i < 10:
            num_vert = font.render(str(i+1), True, BLACK)
            letters_hor = font.render(letters[i], True, BLACK)

            num_vert_width = num_vert.get_width()
            num_vert_height = num_vert.get_height()
            letters_hor_width = letters_hor.get_width()

            #Vert num grid1
            screen.blit(num_vert, (left_margin - (block_size//2+num_vert_width//2),
                                   upper_margin + i*block_size + (block_size//2 - num_vert_height//2)))
            #Hor letters grid1
            screen.blit(letters_hor, (left_margin + i*block_size + (block_size//2 - letters_hor_width//2),
                                      upper_margin + 10 * block_size))

            # Vert num grid2
            screen.blit(num_vert, (left_margin - (block_size // 2 + num_vert_width // 2) + 15 * block_size,
                                   upper_margin + i * block_size + (block_size // 2 - num_vert_height // 2)))
            # Hor letters grid2
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size // 2 - letters_hor_width // 2) + 15 * block_size,
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