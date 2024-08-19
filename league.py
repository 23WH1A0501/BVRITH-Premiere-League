import pygame
import sys
import random
import time
import math
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("BVRITH Premier League")

# Load background images
BG_MAIN_MENU = pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Background_main_menu.jpeg")
BG_PLAYER_CHOICE = pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Background_player_choice.jpeg")
BG_GAMEPLAY = pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Background_gameplay.jpg")
CLICK_SOUND = pygame.mixer.Sound(r'C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Button_click.wav')
BRAVO_SOUND = pygame.mixer.Sound(r'C:\Users\Logins\Downloads\WISE Project Team 1\uploads\BRAVO_SOUND.wav')
OH_NO_SOUND = pygame.mixer.Sound(r'C:\Users\Logins\Downloads\WISE Project Team 1\uploads\OH NO_SOUND.wav')
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\font.ttf", size)

class Button:
    def _init_(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.click_sound = CLICK_SOUND
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            if self.click_sound:
                self.click_sound.play()
            return True
        return False

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def text_input_box(x, y, w, h, text='', font=None):
    base_color = pygame.Color('white')
    active_color = pygame.Color('dodgerblue2')
    color = base_color
    active = False
    text_surface = font.render(text, True, color)
    rect = pygame.Rect(x, y, w, h)
    cursor = pygame.Rect(rect.topright, (3, rect.height))

    def handle_event(event):
        nonlocal active, text, text_surface, color
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = active_color if active else base_color
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    active = False
                    color = base_color
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                text_surface = font.render(text, True, color)
                cursor.topleft = text_surface.get_rect(topleft=(rect.x + 5, rect.y + 5)).topright

    def draw(screen):
        pygame.draw.rect(screen, pygame.Color('black'), rect)  # Use the same color as the background
        pygame.draw.rect(screen, color, rect, 2)
        screen.blit(text_surface, text_surface.get_rect(topleft=(rect.x + 5, rect.y + 5)))
        if active:
            screen.fill(color, cursor)

    return handle_event, draw, lambda: text

def choose_player():
    player1_name = ''
    player2_name = ''
    input_box1 = text_input_box(440, 250, 400, 50, '', get_font(40))
    input_box2 = text_input_box(440, 350, 400, 50, '', get_font(40))
    input_boxes = [input_box1, input_box2]

    player_names_entered = False
    while True:
        CHOOSE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG_PLAYER_CHOICE, (0, 0))

        if not player_names_entered:
            CHOOSE_TEXT = get_font(45).render("Enter Player Names", True, "Black")
            CHOOSE_RECT = CHOOSE_TEXT.get_rect(center=(640, 150))
            SCREEN.blit(CHOOSE_TEXT, CHOOSE_RECT)

            PLAYER1_TEXT = get_font(40).render("Player 1 Name:", True, "Black")
            PLAYER1_RECT = PLAYER1_TEXT.get_rect(center=(220, 275))
            SCREEN.blit(PLAYER1_TEXT, PLAYER1_RECT)

            PLAYER2_TEXT = get_font(40).render("Player 2 Name:", True, "Black")
            PLAYER2_RECT = PLAYER2_TEXT.get_rect(center=(220, 375))
            SCREEN.blit(PLAYER2_TEXT, PLAYER2_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                for input_box in input_boxes:
                    input_box[0](event)

            for input_box in input_boxes:
                input_box[1](SCREEN)

            player1_name = input_box1[2]()
            player2_name = input_box2[2]()

            if player1_name and player2_name:
                CONTINUE_BUTTON = Button(image=None, pos=(640, 500),
                                         text_input="CONTINUE", font=get_font(75), base_color="White",
                                         hovering_color="Green")
                CONTINUE_BUTTON.changeColor(CHOOSE_MOUSE_POS)
                CONTINUE_BUTTON.update(SCREEN)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if CONTINUE_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                            player_names_entered = True
                            break

        else:
            CHOOSE_TEXT = get_font(45).render("Choose who bats first", True, "Black")
            CHOOSE_RECT = CHOOSE_TEXT.get_rect(center=(640, 200))
            SCREEN.blit(CHOOSE_TEXT, CHOOSE_RECT)

            PLAYER1_BUTTON = Button(image=None, pos=(640, 350),
                                    text_input=player1_name, font=get_font(75), base_color="White",
                                    hovering_color="Green")
            PLAYER2_BUTTON = Button(image=None, pos=(640, 500),
                                    text_input=player2_name, font=get_font(75), base_color="White",
                                    hovering_color="Green")

            for button in [PLAYER1_BUTTON, PLAYER2_BUTTON]:
                button.changeColor(CHOOSE_MOUSE_POS)
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAYER1_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                        play_game(1, player1_name, player2_name)
                    if PLAYER2_BUTTON.checkForInput(CHOOSE_MOUSE_POS):
                        play_game(2, player1_name, player2_name)

        pygame.display.update()

def display_message(screen, message, color, duration, sound):
    start_time = pygame.time.get_ticks()
    sound.play()
    clock = pygame.time.Clock()
    while pygame.time.get_ticks() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        message_text = get_font(60).render(message, True, color)
        message_rect = message_text.get_rect(center=(640, 360))
        screen.fill((0, 0, 0))  # Fill screen with black before drawing text
        screen.blit(message_text, message_rect)
        pygame.display.update()
        clock.tick(60)
def generate_trajectory():
    trajectories = []
    for _ in range(30):
        trajectory = []
        start_x, start_y = 1131, 531
        end_x = random.randint(160, 410)
        end_y = 531
        peak_x = random.randint(680, 800)
        peak_y = random.randint(193, 333)

        # Random perturbations to make the path less predictable
        perturbation_x = random.uniform(-50, 50)
        perturbation_y = random.uniform(-30, 30)

        control_x1 = start_x + random.uniform(-50, 50)
        control_y1 = start_y - random.uniform(50, 150)
        control_x2 = peak_x + perturbation_x
        control_y2 = peak_y + perturbation_y

        # Create trajectory points using cubic bezier curve
        for t in range(101):
            t /= 100
            x = (1 - t) ** 3 * start_x + 3 * (1 - t) ** 2 * t * control_x1 + 3 * (1 - t) * t ** 2 * control_x2 + t ** 3 * end_x
            y = (1 - t) ** 3 * start_y + 3 * (1 - t) ** 2 * t * control_y1 + 3 * (1 - t) * t ** 2 * control_y2 + t ** 3 * end_y
            trajectory.append((x, y))

        trajectories.append(trajectory)

    return trajectories



def play_game(first_batter, player1_name, player2_name):
    trajectories = generate_trajectory()

    def display_hits():
        circle_radius = 19  # same size as the ball
        spacing = 50
        y_start = 150

        # Player 1
        x_start_1 = 200
        player1_text = get_font(30).render(player1_name, True, "White")
        player1_text_rect = player1_text.get_rect(center=(x_start_1 - 100, y_start - 40))
        SCREEN.blit(player1_text, player1_text_rect)

        for i in range(6):
            color = (0, 255, 0) if i < player1_hits else (255, 0, 0) if i < (player1_hits + player1_misses) else (255, 255, 255)
            pygame.draw.circle(SCREEN, color, (x_start_1 + i * spacing, y_start), circle_radius)

        # Player 2
        x_start_2 = 1080
        player2_text = get_font(30).render(player2_name, True, "White")
        player2_text_rect = player2_text.get_rect(center=(x_start_2 + 100, y_start - 40))
        SCREEN.blit(player2_text, player2_text_rect)

        for i in range(6):
            color = (0, 255, 0) if i < player2_hits else (255, 0, 0) if i < (player2_hits + player2_misses) else (255, 255, 255)
            pygame.draw.circle(SCREEN, color, (x_start_2 - i * spacing, y_start), circle_radius)

    player1_hits = 0
    player1_misses = 0
    player2_hits = 0
    player2_misses = 0
    current_player = first_batter
    game_over = False
    ball_hit = False
    ball_horizontal = True
    ball_speed = 15  # Increased ball speed for more challenging gameplay

    bat_image = pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\bat.png")
    bat_image = pygame.transform.scale(bat_image, (30, 120))  # Scale to the correct size (width: 30px, height: appropriate)

    ball_image = pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\ball.png")
    ball_image = pygame.transform.scale(ball_image, (38, 38))  # Scale to the correct size

    ball_rect = ball_image.get_rect(center=(1280, 531))
    bat_rect = bat_image.get_rect(center=(160, 531))
    clock = pygame.time.Clock()
    ball_trajectory = random.choice(trajectories)
    ball_index = 0

    # Flags for bat movement
    move_left = False
    move_right = False
    move_up = False
    move_down = False

    def swing_bat():
        for angle in range(0, 106, 5):  # Swing down to 105 degrees
            rotated_image = pygame.transform.rotate(bat_image, angle)
            new_rect = rotated_image.get_rect(center=(bat_rect.x + 15, bat_rect.y))  # Adjusted to rotate around top end
            SCREEN.blit(BG_GAMEPLAY, (0, 0))
            display_hits()
            SCREEN.blit(ball_image, ball_rect)
            SCREEN.blit(rotated_image, new_rect.topleft)
            pygame.display.update()
            clock.tick(60)
        for angle in range(105, -1, -5):  # Swing back to 0 degrees
            rotated_image = pygame.transform.rotate(bat_image, angle)
            new_rect = rotated_image.get_rect(center=(bat_rect.x + 15, bat_rect.y))  # Adjusted to rotate around top end
            SCREEN.blit(BG_GAMEPLAY, (0, 0))
            display_hits()
            SCREEN.blit(ball_image, ball_rect)
            SCREEN.blit(rotated_image, new_rect.topleft)
            pygame.display.update()
            clock.tick(60)

    while not game_over:
        if current_player == 1 and player1_hits + player1_misses >= 6:
            current_player = 2
        elif current_player == 2 and player2_hits + player2_misses >= 6:
            game_over = True
            break

        # Reset bat and ball position
        bat_rect.x = 160
        bat_rect.y = 531
        ball_rect.x = 1280
        ball_rect.y = 531
        ball_hit = False
        ball_horizontal = True
        ball_index = 0
        ball_trajectory = random.choice(trajectories)

        # Display alert for 2 seconds
        for i in range(120):  # Assuming 60 frames per second
            SCREEN.blit(BG_GAMEPLAY, (0, 0))
            alert_text = get_font(45).render("Ball starts in 2 seconds", True, "Red")
            alert_rect = alert_text.get_rect(center=(640, 360))
            SCREEN.blit(alert_text, alert_rect)
            display_hits()
            pygame.display.update()
            clock.tick(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    if event.key == pygame.K_RIGHT:
                        move_right = True
                    if event.key == pygame.K_UP:
                        move_up = True
                    if event.key == pygame.K_DOWN:
                        move_down = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_left = False
                    if event.key == pygame.K_RIGHT:
                        move_right = False
                    if event.key == pygame.K_UP:
                        move_up = False
                    if event.key == pygame.K_DOWN:
                        move_down = False

            if move_left:
                bat_rect.x -= 5
            if move_right:
                bat_rect.x += 5
            if move_up:
                bat_rect.y -= 5
            if move_down:
                bat_rect.y += 5

            if ball_horizontal:
                ball_rect.x -= ball_speed
                if ball_rect.x <= 1131:
                    ball_horizontal = False

            elif not ball_hit:
                if ball_index < len(ball_trajectory):
                    ball_rect.center = ball_trajectory[ball_index]
                    ball_index += 1
                else:
                    if current_player == 1:
                        player1_misses += 1
                        display_message(SCREEN, "OH NO!", (255, 0, 0), 4000, OH_NO_SOUND)
                    else:
                        player2_misses += 1
                        display_message(SCREEN, "OH NO!", (255, 0, 0), 4000, OH_NO_SOUND)
                    break
            else:
                ball_rect.x += int(ball_speed * math.cos(ball_angle))
                ball_rect.y -= int(ball_speed * math.sin(ball_angle))
                if ball_rect.right < 0 or ball_rect.left > 1280 or ball_rect.top < 0 or ball_rect.bottom > 720:
                    break

            if bat_rect.colliderect(ball_rect) and not ball_hit:
                ball_hit = True
                swing_bat()
                ball_speed = random.randint(10, 20)
                ball_angle = random.uniform(math.pi / 4, 3 * math.pi / 4)  # Random angle between 45 and 135 degrees
                if current_player == 1:
                    player1_hits += 1
                    display_message(SCREEN, "BRAVO!", (0, 255, 0), 4000, BRAVO_SOUND)

                else:
                    player2_hits += 1
                    display_message(SCREEN, "BRAVO!", (0, 255, 0), 4000, BRAVO_SOUND)

            SCREEN.blit(BG_GAMEPLAY, (0, 0))
            display_hits()
            SCREEN.blit(ball_image, ball_rect)
            SCREEN.blit(bat_image, bat_rect)
            pygame.display.update()
            clock.tick(60)

    # Display the final result
    winner_text = ""
    if player1_hits > player2_hits:
        winner_text = f"{player1_name} wins by {player1_hits - player2_hits} runs!"
    elif player2_hits > player1_hits:
        winner_text = f"{player2_name} wins by {player2_hits - player1_hits} runs!"
    else:
        winner_text = "It's a tie!"

    while True:
        SCREEN.blit(BG_GAMEPLAY, (0, 0))
        result_text = get_font(45).render(winner_text, True, "White")
        result_rect = result_text.get_rect(center=(640, 360))
        SCREEN.blit(result_text, result_rect)

        MENU_BUTTON = Button(image=None, pos=(640, 500),
                             text_input="MAIN MENU", font=get_font(75), base_color="White", hovering_color="Green")
        MENU_BUTTON.changeColor(pygame.mouse.get_pos())
        MENU_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_menu()

        pygame.display.update()



def main_menu():
    while True:
        SCREEN.blit(BG_MAIN_MENU, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(40).render("BVRITH PREMIER LEAGUE", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(r"C:\Users\Logins\Downloads\WISE Project Team 1\uploads\Quit Rect.png"), pos=(640, 400),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_player()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if _name_ == "_main_":
    main_menu()
