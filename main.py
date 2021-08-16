import pygame
import random
import copy

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BLUE = (0, 153, 153)
LIGHT_GRAY = (192, 192, 192)
RED = (255, 0, 0)


block_size = 40
left_margin = 50
upper_margin = 60

size = (left_margin + 30 * block_size, upper_margin + 15 * block_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

pygame.init()

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Okręgi")

font_size = int(block_size / 1.5)

font = pygame.font.SysFont('notosans', font_size)

computer_available_to_fire_set = {(a, b) for a in range(16, 25) for b in range(1, 11)}
around_last_computer_hit_set = set()
hit_blocks = set()
dotted_set = set()
dotted_set_for_computer_not_to_shoot = set()
hit_blocks_for_computer_not_to_shoot = set()
last_hits_list = []
destroyed_ships_list = []

class Grid:
    def __init__(self, title, offset):
        self.title = title
        self.offset = offset
        self.draw_grid()
        self.sign_grids()
        self.add_nums_letters_to_grid()

    def draw_grid(self):
        for i in range(11):

            #Hor lines
            pygame.draw.line(screen, BLACK, (left_margin+self.offset, upper_margin+i*block_size),
                             (left_margin+10*block_size+self.offset, upper_margin+i*block_size), 1)
            #Vert lines
            pygame.draw.line(screen, BLACK, (left_margin+i*block_size+self.offset, upper_margin),
                             (left_margin+i*block_size+self.offset, upper_margin+10*block_size), 1)

    def add_nums_letters_to_grid(self):
        for i in range(10):
            num_vert = font.render(str(i+1), True, BLACK)
            letters_hor = font.render(LETTERS[i], True, BLACK)

            num_vert_width = num_vert.get_width()
            num_vert_height = num_vert.get_height()
            letters_hor_width = letters_hor.get_width()

            #Vert num grid1
            screen.blit(num_vert, (left_margin - (block_size//2+num_vert_width//2)+self.offset,
                                   upper_margin + i*block_size + (block_size//2 - num_vert_height//2)))
            #Hor letters grid1
            screen.blit(letters_hor, (left_margin + i * block_size + (block_size//2 - letters_hor_width//2)+self.offset,
                                      upper_margin + 10 * block_size))

    def sign_grids(self):
        player = font.render(self.title, True, BLACK)
        sign_width = player.get_width()
        screen.blit(player, (left_margin + 5 * block_size - sign_width//2+self.offset, upper_margin - block_size//2 - font_size))

class Button:
    def __init__(self, x_offset, button_title, message_to_show):
        self.__title = button_title
        self.__title_width, self.__title_height = font.size(self.__title)
        self.__message = message_to_show
        self.__button_width = self.__title_width + block_size
        self.__button_height = self.__title_height + block_size
        self.__x_start = x_offset
        self.__y_start = upper_margin + 10 * block_size + self.__button_height

        self.rect_for_draw = self.__x_start, self.__y_start, self.__button_width, self.__button_height
        self.rect = pygame.Rect(self.rect_for_draw)

        self.__rect_for_button_title = self.__x_start + self.__button_width / 2 - self.__title_width / 2, self.__y_start + self.__button_height / 2 - self.__title_height / 2
        self.__color = BLACK

    def draw_button(self, color=None):
        if not color:
            color = self.__color
        pygame.draw.rect(screen, color, self.rect_for_draw)
        text_to_blit = font.render(self.__title, True, WHITE)
        screen.blit(text_to_blit, self.__rect_for_button_title)


    def change_color_on_hover(self):
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse):
            self.draw_button(GREEN_BLUE)

    def print_message_for_button(self):
        message_width, message_height = font.size(self.__message)
        rect_for_message = self.__x_start / 2 - message_width / 2, self.__y_start + self.__button_height / 2 - message_height / 2
        text = font.render(self.__message, True, BLACK)
        screen.blit(text, rect_for_message)




class AutoShips:
    def __init__(self, offset):
        self.offset = offset
        self.available_blocks = {(x, y) for x in range(1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.populate_grid()

    def create_start_block(self, available_blocks):
        x_or_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(available_blocks))
        return x, y, x_or_y, str_rev

    def create_ship(self, number_of_blocks, available_blocks):
        ship_coordinates = []
        x, y, x_or_y, str_rev = self.create_start_block(available_blocks)
        for _ in range(number_of_blocks):
            ship_coordinates.append((x, y))
            if not x_or_y:
                str_rev, x = self.get_new_block_for_ship(
                    x, str_rev, x_or_y, ship_coordinates)
            else:
                str_rev, y = self.get_new_block_for_ship(
                    y, str_rev, x_or_y, ship_coordinates)
        if self.if_ship_valid(ship_coordinates):
            return ship_coordinates
        return self.create_ship(number_of_blocks, available_blocks)

    def get_new_block_for_ship(self, coor, str_rev, x_or_y, ship_coordinates):
        if(coor <= 1-self.offset*(x_or_y - 1) and str_rev == -1) or (coor >= 10-self.offset*(x_or_y - 1) and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coordinates[0][x_or_y] + str_rev
        else:
            return str_rev, ship_coordinates[-1][x_or_y] + str_rev

    def if_ship_valid(self, new_ship):
        ship = set(new_ship)
        return ship.issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    def update_available_blocks_for_creating_ships(self, new_ship):
        for elem in new_ship:
            for k in range(-1, 2):
                for m in range(-1, 2):
                    if 0+self.offset < (elem[0]+k) < 11+self.offset and 0 < (elem[1]+m) < 11:
                        self.available_blocks.discard((elem[0]+k, elem[1]+m))

    def populate_grid(self):
        ships_coordinates_list = []
        for number_of_blocks in range(4, 0, -1):
            for _ in range(5-number_of_blocks):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list

def ship_is_valid(ship_set, blocks_for_manual_drawing):
    return ship_set.isdisjoint(blocks_for_manual_drawing)

def check_ships_numbers(ship, num_ships_list):
    return (5 - len(ship)) > num_ships_list[len(ship) - 1]

def update_used_blocks(ship, used_blocks_set):
    for block in ship:
        for i in range(-1, 2):
            for j in range(-1, 2):
                used_blocks_set.add((block[0] + i, block[1] + j))
    return used_blocks_set

computer = AutoShips(0)
#human = AutoShips(15)
computer_ships_working = copy.deepcopy(computer.ships)
#human_ships_working = copy.deepcopy(human.ships)

auto_button_place = left_margin + 17 * block_size
manual_button_place = left_margin + 20 * block_size
how_to_create_ships_message = "Jak chcesz umieścić statki? Naciśnij przycisk"
auto_button = Button(auto_button_place, "Auto", how_to_create_ships_message)
manual_button = Button(manual_button_place, "Ręcznie", how_to_create_ships_message)
undo_message = "Żeby zmienić ostatni okręg naciśnij przycisk"
undo_button_place = left_margin + 12 * block_size
undo_button = Button(undo_button_place, "Skasować", undo_message)

def draw_ships(ships_coordinates_list):
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # hor and 1block ships
        ship_width = block_size * len(ship)
        ship_height = block_size
        #vert
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = block_size * (x_start - 1) + left_margin
        y = block_size * (y_start - 1) + upper_margin
        pygame.draw.rect(
            screen, BLACK, ((x, y), (ship_width, ship_height)), width=block_size//10)


def computer_shoots(set_to_shoot_from):
    pygame.time.delay(500)
    computer_fired_blocked = random.choice(tuple(set_to_shoot_from))
    computer_available_to_fire_set.discard(computer_fired_blocked)
    return computer_fired_blocked


def check_hit_or_miss(fired_block, opponents_ships_list, computer_turn, opponents_ships_list_original_copy, opponents_ships_set):
    for elem in opponents_ships_list:
        diagonal_only = True
        if fired_block in elem:
            ind = opponents_ships_list.index(elem)
            if len(elem) == 1:
                diagonal_only = False
            update_dotted_and_hit_sets(fired_block, computer_turn, diagonal_only)
            elem.remove(fired_block)
            opponents_ships_set.discard(fired_block)
            if computer_turn:
                last_hits_list.append(fired_block)
                update_around_last_computer_hit(fired_block)
            if not elem:
                update_destroyed_ships(ind, computer_turn, opponents_ships_list_original_copy)
                if computer_turn:
                    last_hits_list.clear()
                    around_last_computer_hit_set.clear()
                else:
                    destroyed_ships_list.append(computer.ships[ind])

            return True
    add_missed_block_to_dotted_set(fired_block)
    if computer_turn:
        update_around_last_computer_hit(fired_block, False)
    return False

def add_missed_block_to_dotted_set(fired_block):
    dotted_set.add(fired_block)
    dotted_set_for_computer_not_to_shoot.add(fired_block)

def update_destroyed_ships(ind, computer_turn, opponents_ships_list_original_copy):
    ship = sorted(opponents_ships_list_original_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], computer_turn, False)


def update_around_last_computer_hit(fired_block, computer_hits=True):
    global around_last_computer_hit_set, computer_available_to_fire_set
    if computer_hits and fired_block in around_last_computer_hit_set:
        around_last_computer_hit_set = computer_hits_twice()

    elif computer_hits and fired_block not in around_last_computer_hit_set:
        computer_first_hit(fired_block)
    elif not computer_hits:
        around_last_computer_hit_set.discard(fired_block)
    around_last_computer_hit_set -= dotted_set_for_computer_not_to_shoot
    around_last_computer_hit_set -= hit_blocks_for_computer_not_to_shoot
    computer_available_to_fire_set -= around_last_computer_hit_set
    computer_available_to_fire_set -= dotted_set_for_computer_not_to_shoot

def computer_first_hit(fired_block):
    xhit, yhit = fired_block
    if 16 < xhit:
        around_last_computer_hit_set.add((xhit - 1, yhit))
    if xhit < 25:
        around_last_computer_hit_set.add((xhit + 1, yhit))
    if 1 < yhit:
        around_last_computer_hit_set.add((xhit, yhit - 1))
    if yhit < 10:
        around_last_computer_hit_set.add((xhit, yhit + 1))

def computer_hits_twice():
    last_hits_list.sort()
    new_around_last_hit_set = set()
    for i in range(len(last_hits_list) - 1):
        x1 = last_hits_list[i][0]
        x2 = last_hits_list[i+1][0]
        y1 = last_hits_list[i][1]
        y2 = last_hits_list[i+1][1]
        if x1 == x2:
            if y1 > 1:
                new_around_last_hit_set.add((x1, y1 - 1))
            if y2 < 10:
                new_around_last_hit_set.add((x1, y2 + 1))

        elif y1 == y2:
            if x1 > 16:
                new_around_last_hit_set.add((x1 - 1, y1))
            if x2 < 25:
                new_around_last_hit_set.add((x2 + 1, y1))
    return new_around_last_hit_set

def update_dotted_and_hit_sets(fired_block, computer_turn, diagonal_only=True):
    global dotted_set
    x, y = fired_block
    a = 15 * computer_turn
    b = 11 + 15 * computer_turn
    hit_blocks_for_computer_not_to_shoot.add(fired_block)
    hit_blocks.add(fired_block)
    for i in range(-1, 2):
        for j in range(-1, 2):
            if(not diagonal_only or i !=0 and j != 0) and a < x + i < b and 0 < y + j < 11:
                add_missed_block_to_dotted_set((x + i, y + j))
    dotted_set -= hit_blocks


def draw_from_dotted_set(dotted_set):
    for elem in dotted_set:
        pygame.draw.circle(screen, BLACK, (block_size * (elem[0] - 0.5) + left_margin, block_size * (elem[1] - 0.5) + upper_margin), block_size//6)

def draw_hit_blocks(hit_blocks):
    for block in hit_blocks:
        x1 = block_size * (block[0] - 1) + left_margin
        y1 = block_size * (block[1] - 1) + upper_margin
        pygame.draw.line(screen, BLACK, (x1, y1), (x1+block_size, y1+block_size), block_size//6)
        pygame.draw.line(screen, BLACK, (x1, y1 + block_size), (x1+block_size, y1), block_size//6)

def show_message_rect_center(text, rect, which_font=font, color=RED):
    text_width, text_height = which_font.size(text)
    text_rect = pygame.Rect(rect)
    x_start = text_rect.centerx - text_width / 2
    y_start = text_rect.centery - text_height / 2
    background_rect = pygame.Rect(x_start - block_size / 2, y_start, text_width + block_size, text_height)
    text_to_blit = which_font.render(text, True, color)
    screen.fill(WHITE, background_rect)
    screen.blit(text_to_blit, (x_start, y_start))


def main():
    game_over = False
    computer_turn = False
    ship_creation_not_decided = True
    ships_not_created = True
    drawing = False
    start = (0, 0)
    ships_size = (0, 0)


    rect_for_grids = (0, 0, size[0], upper_margin + 12 * block_size)
    rect_for_messages_and_buttons = (0, upper_margin + 11 * block_size, size[0], 5 * block_size)
    message_rect_for_drawing_ships = (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2],
                                      upper_margin + 11 * block_size,
                                      size[0] - (undo_button.rect_for_draw[0] + undo_button.rect_for_draw[2]), 4 * block_size)

    human_ships_to_draw = []
    used_blocks_for_manual_drawing = set()
    num_ships_list = [0, 0, 0, 0]
    human_ships_set = set()


    screen.fill(WHITE)
    computer_grid = Grid("COMPUTER", 0)
    human_grid = Grid("HUMAN", 15 * block_size)
    #draw_ships(computer.ships)
    #draw_ships(human.ships)
    pygame.display.update()

    while ship_creation_not_decided:
        auto_button.draw_button()
        manual_button.draw_button()
        auto_button.change_color_on_hover()
        manual_button.change_color_on_hover()
        auto_button.print_message_for_button()

        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                ship_creation_not_decided = False
                ships_not_created = False
            #if AUTO button is pressed - create human ships automaticaly
            elif event.type == pygame.MOUSEBUTTONDOWN and auto_button.rect.collidepoint(mouse):
                print("Clicked AUTO", event.pos)
                human = AutoShips(15)
                human_ships_to_draw = human.ships
                human_ships_set = human.ships_set
                human_ships_working = copy.deepcopy(human.ships)
                ship_creation_not_decided = False
                ships_not_created = False
            elif event.type == pygame.MOUSEBUTTONDOWN and manual_button.rect.collidepoint(mouse):
                ship_creation_not_decided = False

        pygame.display.update()
        screen.fill(WHITE, rect_for_messages_and_buttons)


    while ships_not_created:
        screen.fill(WHITE, rect_for_grids)
        computer_grid = Grid("Computer", 0)
        human_grid = Grid("Human", 15 * block_size)
        undo_button.draw_button()
        undo_button.print_message_for_button()
        undo_button.change_color_on_hover()
        mouse = pygame.mouse.get_pos()
        if not human_ships_to_draw:
            undo_button.draw_button(LIGHT_GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ships_not_created = False
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                x_start, y_start = event.pos
                start = x_start, y_start
                ships_size = (0, 0)
            elif drawing and event.type == pygame.MOUSEMOTION:
                x_end, y_end = event.pos
                end = x_end, y_end
                ships_size = x_end - x_start, y_end - y_start
            elif drawing and event.type == pygame.MOUSEBUTTONUP:
                x_end, y_end = event.pos
                drawing = False
                ships_size = (0, 0)
                start_block = ((x_start - left_margin) // block_size + 1, (y_start - upper_margin) // block_size + 1)
                end_block = ((x_end - left_margin) // block_size + 1, (y_end - upper_margin) // block_size + 1)
                if start_block > end_block:
                    start_block, end_block = end_block, start_block
                temp_ship = []
                if 15 < start_block[0] < 26 and 0 < start_block[1] < 11 and 15 < end_block[0] < 26 and 0 < end_block[1] < 11:
                    screen.fill(WHITE, message_rect_for_drawing_ships)
                    if start_block[0] == end_block[0] and (end_block[1] - start_block[1]) < 4:
                        for block in range(start_block[1], end_block[1] + 1):
                            temp_ship.append((start_block[0], block))
                    elif start_block[1] == end_block[1] and (end_block[0] - start_block[0]) < 4:
                        for block in range(start_block[0], end_block[0] + 1):
                            temp_ship.append((block, start_block[1]))
                    else:
                        show_message_rect_center("Okręg jest za duży!", message_rect_for_drawing_ships)
                else:
                    show_message_rect_center("Statek poza siatką!", message_rect_for_drawing_ships)
                if temp_ship:
                    temp_ship_set = set(temp_ship)
                    if ship_is_valid(temp_ship_set, used_blocks_for_manual_drawing):
                        if check_ships_numbers(temp_ship, num_ships_list):
                            num_ships_list[len(temp_ship) - 1] += 1
                            human_ships_to_draw.append(temp_ship)
                            human_ships_set |= temp_ship_set
                            used_blocks_for_manual_drawing = update_used_blocks(temp_ship, used_blocks_for_manual_drawing)
                        else:
                            show_message_rect_center(f"Dużo {len(temp_ship)}-mejscowych okręgów.", message_rect_for_drawing_ships)
                    else:
                        show_message_rect_center("Okręgi dotykają się!", message_rect_for_drawing_ships)
            if len(human_ships_to_draw) == 10:
                ships_not_created = False
                human_ships_working = copy.deepcopy(human_ships_to_draw)
                screen.fill(WHITE, rect_for_messages_and_buttons)
        pygame.draw.rect(screen, BLACK, (start, ships_size), 3)
        draw_ships(human_ships_to_draw)
        pygame.display.update()



    while not game_over:
        draw_ships(human_ships_to_draw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif not computer_turn and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (left_margin < x < left_margin + 10 * block_size) and (upper_margin < y < upper_margin + 10 * block_size):
                    fired_block = ((x - left_margin) // block_size + 1, (y - upper_margin) // block_size + 1)
                    computer_turn = not check_hit_or_miss(fired_block, computer_ships_working, False, computer.ships, computer.ships_set)
        if computer_turn:
            set_to_shoot_from = computer_available_to_fire_set
            if around_last_computer_hit_set:
                set_to_shoot_from = around_last_computer_hit_set
            fired_block = computer_shoots(set_to_shoot_from)
            computer_turn = check_hit_or_miss(fired_block, human_ships_working, True, human.ships, human.ships_set)

        draw_from_dotted_set(dotted_set)
        draw_hit_blocks(hit_blocks)
        draw_ships(destroyed_ships_list)
        pygame.display.update()

main()
pygame.quit()