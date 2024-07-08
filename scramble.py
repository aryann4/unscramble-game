import pygame
import sys
import requests
import time
import sqlite3
import random
from wonderwords import RandomWord
pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Unscramble')
game_font = pygame.font.Font('Itim-Regular.ttf', 48)
small_font = pygame.font.Font('Itim-Regular.ttf', 32)
scramword_font = pygame.font.Font('Itim-Regular.ttf', 58)
time_font = pygame.font.Font('Itim-Regular.ttf', 42)

GREEN = (0, 200, 0)
LIGHT_GREEN = (220, 255, 200)
DARK_GREEN = (0, 150, 0)
BLACK = (0, 0, 0)
GRAY = (150, 150, 150)
BLUE = (100, 150, 255)
DARK_BLUE = (70, 120, 225)
RED1 = (255, 0, 0)
RED2 = (204, 0 , 0)
RED3 = (153, 0, 0)
ORANGE = (255, 165, 0)

conn = sqlite3.connect('unscramble.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS standard_scores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              score INTEGER,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS timed_scores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              words_typed INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS ultimate_scores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              words_typed INTEGER)''')
conn.commit()

# Random Word API (replaced with wonderwords library)
def fetch_words(num_words):
    r = RandomWord()
    response = r.random_words(num_words, word_min_length=4, word_max_length=15)
    filtered_words = [word for word in response if '-' not in word]

    # url = f"https://random-word-api.herokuapp.com/word?number={num_words}"
    # response = requests.get(url)
    # return response.json()

    return filtered_words

def shuffle_word(word):
    word = list(word)
    random.shuffle(word)
    return ''.join(word)

def draw_text(text, font, color, surface, x, y, moving = False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    if moving:
        surface.blit(text_obj, (x, y + 2))
    else:
        surface.blit(text_obj, text_rect)

def display_home_screen():
    screen.fill(LIGHT_GREEN)
    draw_text('Unscramble!!!', game_font, BLACK, screen, 255, 100)
    game_modes_button = pygame.Rect(250, 250, 300, 50)
    leaderboards_button = pygame.Rect(250, 350, 300, 50)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if game_modes_button.collidepoint(mouse_pos):
                    display_game_modes_screen()
                elif leaderboards_button.collidepoint(mouse_pos):
                    display_leaderboards_screen()

        mouse_pos = pygame.mouse.get_pos()
        if game_modes_button.collidepoint(mouse_pos):
            game_modes_color = DARK_BLUE
            gmline = True
        else:
            game_modes_color = BLUE
            gmline = False
        if leaderboards_button.collidepoint(mouse_pos):
            leaderboards_color = DARK_GREEN
            lbline = True
        else:
            leaderboards_color = GREEN
            lbline = False
        pygame.draw.rect(screen, game_modes_color, game_modes_button)
        draw_text('Game Modes', small_font, BLACK, screen, 310, 255, gmline)
        pygame.draw.rect(screen, leaderboards_color, leaderboards_button)
        draw_text('Leaderboards', small_font, BLACK, screen, 305, 355, lbline)
        pygame.display.flip()

def display_game_modes_screen():
    screen.fill(LIGHT_GREEN)
    draw_text('Game Modes', game_font, BLACK, screen, 265, 100)
    standard_button = pygame.Rect(250, 200, 300, 50)
    timed_button = pygame.Rect(250, 300, 300, 50)
    ultimate_button = pygame.Rect(250, 400, 300, 50)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if standard_button.collidepoint(mouse_pos):
                    start_standard_game()
                elif timed_button.collidepoint(mouse_pos):
                    start_timed_game()
                elif ultimate_button.collidepoint(mouse_pos):
                    start_ultimate_game()
                else:
                    display_home_screen()
        mouse_pos = pygame.mouse.get_pos()
        if standard_button.collidepoint(mouse_pos):
            stan_modes_color = DARK_BLUE
            smline = True
        else:
            stan_modes_color = BLUE
            smline = False
        if timed_button.collidepoint(mouse_pos):
            timed_modes_color = DARK_BLUE
            tmline = True
        else:
            timed_modes_color = BLUE
            tmline = False
        if ultimate_button.collidepoint(mouse_pos):
            ultim_modes_color = DARK_BLUE
            umline = True
        else:
            ultim_modes_color = BLUE
            umline = False
        pygame.draw.rect(screen, stan_modes_color, standard_button)
        draw_text('Standard', small_font, BLACK, screen, 335, 205, smline)
        pygame.draw.rect(screen, timed_modes_color, timed_button)
        draw_text('Timed', small_font, BLACK, screen, 352, 305, tmline)
        pygame.draw.rect(screen, ultim_modes_color, ultimate_button)
        draw_text('Ultimate', small_font, BLACK, screen, 335, 405, umline)
        pygame.display.flip()

def start_standard_game():
    words = fetch_words(15)
    # for word in words:
    #     print(word)
    # print('---------------------------------')
    play_game(words)

def start_timed_game():
    words = fetch_words(30)
    # for word in words:
    #     print(word)
    # print('---------------------------------')
    play_timed_game(words)

def start_ultimate_game():
    words = fetch_words(45)
    # for word in words:
    #     print(word)
    # print('---------------------------------')
    play_ultimate_game(words)

def play_game(words):
    current_word_index = 0
    current_word = words[current_word_index]
    typed_text = ['_'] * len(current_word)
    current_index = 0
    word_typed_correctly = False  
    scrambled_word = shuffle_word(current_word)  
    correct_num = 0
    start_time = time.time()
    end_time = None  
    word_change_time = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and current_index > 0:
                    current_index -= 1
                    typed_text[current_index] = '_'
                elif event.unicode.isalpha() and current_index < len(typed_text):
                    typed_text[current_index] = event.unicode
                    current_index += 1
                    if ''.join(typed_text) == current_word:
                        word_typed_correctly = True
                        if current_word_index == 0 or word_change_time is None:
                            word_change_time = time.time() + 1

        if word_typed_correctly and time.time() >= word_change_time:
            current_word_index += 1
            correct_num += 1
            if current_word_index < len(words):
                current_word = words[current_word_index]
                typed_text = ['_'] * len(current_word)
                current_index = 0
                word_typed_correctly = False  
                scrambled_word = shuffle_word(current_word)  
                word_change_time = None
            else:
                end_time = time.time() 
                running = False 

        screen.fill(LIGHT_GREEN)
        draw_text(scrambled_word, scramword_font, BLACK, screen, 50, 30)
        draw_text(' '.join(typed_text), game_font, BLACK, screen, 60, 400)
        draw_text(f'{correct_num}/{len(words)}', game_font, BLACK, screen, 605, 400)
        elapsed_time = int(time.time() - start_time)
        draw_text(f'Time: {elapsed_time} sec', time_font, BLACK, screen, 510, 45)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    total_time = int(end_time - start_time)    
    name_entered = False
    player_name = ''
    while not name_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  
                elif event.unicode.isalnum():
                    player_name += event.unicode
        screen.fill(LIGHT_GREEN)
        draw_text('You typed all the words correctly!', game_font, BLACK, screen, 65, 100)
        draw_text(f'Time: {total_time} seconds', small_font, BLACK, screen, 65, 225)
        draw_text(f'Enter Your Name: {player_name}', small_font, BLACK, screen, 65, 350)
        pygame.display.flip()

    update_standard_leaderboard(player_name, total_time)
    display_home_screen()

def play_timed_game(words):
    current_word_index = 0
    current_word = words[current_word_index]
    typed_text = ['_'] * len(current_word)
    current_index = 0
    word_typed_correctly = False  
    scrambled_word = shuffle_word(current_word)  
    words_unscrambeled = 0
    start_time = time.time()
    end_time = start_time + 121  # 2 minute timer
    word_change_time = 0

    while time.time() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and current_index > 0:
                    current_index -= 1
                    typed_text[current_index] = '_'
                elif event.unicode.isalpha() and current_index < len(typed_text):
                    typed_text[current_index] = event.unicode
                    current_index += 1

                    if ''.join(typed_text) == current_word:
                        word_typed_correctly = True
                        if current_word_index == 0 or word_change_time is None:
                            word_change_time = time.time() + 1

        if word_typed_correctly and time.time() >= word_change_time:
            words_unscrambeled += 1
            current_word_index += 1
            end_time += 4
            if current_word_index < len(words):
                current_word = words[current_word_index]
                typed_text = ['_'] * len(current_word)
                current_index = 0
                word_typed_correctly = False 
                scrambled_word = shuffle_word(current_word)  
                word_change_time = None

        screen.fill(LIGHT_GREEN)
        draw_text(scrambled_word, scramword_font, BLACK, screen, 50, 30)
        draw_text(' '.join(typed_text), game_font, BLACK, screen, 60, 400) 
        draw_text(f'{words_unscrambeled}', game_font, BLACK, screen, 610, 400)
        elapsed_time = int(end_time - time.time())
        draw_text(f'Time: {elapsed_time} sec', time_font, BLACK, screen, 510, 45)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    screen.fill(LIGHT_GREEN)
    draw_text('Time\'s up!!!', game_font, BLACK, screen, 65, 100)
    draw_text(f'Words Unscrambeled: {words_unscrambeled}', small_font, BLACK, screen, 65, 225)
    pygame.display.flip()
    if words_unscrambeled == 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    display_home_screen()

    name_entered = False
    player_name = ''
    while not name_entered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_name:
                        name_entered = True
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  
                elif event.unicode.isalnum():
                    player_name += event.unicode
        screen.fill(LIGHT_GREEN)
        draw_text('Time\'s up!!!', game_font, BLACK, screen, 65, 100)
        draw_text(f'Words Unscrambeled: {words_unscrambeled}', small_font, BLACK, screen, 65, 225)
        draw_text(f'Enter Your Name: {player_name}', small_font, BLACK, screen, 65, 350)
        pygame.display.flip()

    update_timed_leaderboard(player_name, words_unscrambeled)
    display_home_screen()


def play_ultimate_game(words):
    screen.fill(LIGHT_GREEN)
    draw_text('Unscramble Words:', game_font, BLACK, screen, 200, 50)
    current_word_index = 0
    strikes = 0
    words_unscrambled = 0
    shuffled_words = [shuffle_word(word) for word in words]
    current_word = shuffled_words[current_word_index]
    typed_text = ['_'] * len(current_word)  
    strike_text = ''
    strike_color = RED1
    running = True

    while running:
        screen.fill(LIGHT_GREEN)
        draw_text(current_word, scramword_font, BLACK, screen, 50, 30)
        draw_text(' '.join(typed_text), game_font, BLACK, screen, 60, 400)
        draw_text(strike_text, game_font, strike_color, screen, 570, 40)  
        draw_text(f'{words_unscrambled}', game_font, BLACK, screen, 605, 400)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if '_' not in typed_text:
                        if ''.join(typed_text) == words[current_word_index]:
                            words_unscrambled += 1
                            current_word_index += 1
                            if current_word_index < len(words):
                                current_word = shuffled_words[current_word_index]
                                typed_text = ['_'] * len(current_word)  
                            else:
                                running = False  
                        else:
                            strikes += 1
                            if strikes > 3:
                                running = False  
                                break
                            strike_text += 'X' 
                            if strikes == 2:
                                strike_color = RED2
                            elif strikes == 3:
                                strike_color = RED3
                            typed_text = ['_'] * len(current_word) 
                elif event.key == pygame.K_BACKSPACE:
                    if strikes < 4: 
                        for i in range(len(typed_text) - 1, -1, -1):
                            if typed_text[i].islower():  
                                typed_text[i] = '_'  
                                break  
                elif event.unicode.isalpha() and '_' in typed_text:
                    idx = typed_text.index('_')
                    typed_text[idx] = event.unicode.lower()
        
        pygame.display.flip()
        pygame.time.Clock().tick(30)  
    
    screen.fill(LIGHT_GREEN)
    draw_text('Game Over!', game_font, BLACK, screen, 220, 100)
    draw_text(f'Words Unscrambled: {words_unscrambled}', small_font, BLACK, screen, 210, 200)
    pygame.display.flip()
    if words_unscrambled == 0:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    display_home_screen()
    else:
        name_entered = False
        player_name = ''
        while not name_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        name_entered = True
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]  
                    elif event.unicode.isalnum():
                        player_name += event.unicode
            screen.fill(LIGHT_GREEN)
            draw_text('Game Over!', game_font, BLACK, screen, 65, 100)
            draw_text(f'Unscrambled Words: {words_unscrambled}', small_font, BLACK, screen, 65, 225)
            draw_text(f'Enter Your Name: {player_name}', small_font, BLACK, screen, 65, 350)
            pygame.display.flip()
        update_ultimate_leaderboard(player_name, words_unscrambled)
        display_home_screen()

def play():
    display_home_screen()

def update_standard_leaderboard(name, score):
    c.execute("INSERT INTO standard_scores (name, score) VALUES (?, ?)",
              (name, score))
    conn.commit()
def update_timed_leaderboard(name, words_typed):
    c.execute("INSERT INTO timed_scores (name, words_typed) VALUES (?, ?)",
              (name, words_typed))
    conn.commit()
def update_ultimate_leaderboard(name, words_typed):
    c.execute("INSERT INTO ultimate_scores (name, words_typed) VALUES (?, ?)",
              (name, words_typed))
    conn.commit()

def display_leaderboards_screen():
    screen.fill(LIGHT_GREEN)
    draw_text('Leaderboards', game_font, BLACK, screen, 245, 85)
    standard_leader_button = pygame.Rect(220, 200, 340, 50)
    timed_leader_button = pygame.Rect(245, 300, 295, 50)
    ultimate_leader_button = pygame.Rect(220, 400, 340, 50)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if standard_leader_button.collidepoint(mouse_pos):
                    display_standard_leaderboard()
                elif timed_leader_button.collidepoint(mouse_pos):
                    display_timed_leaderboard()
                elif ultimate_leader_button.collidepoint(mouse_pos):
                    display_ultimate_leaderboard()
                else:
                    display_home_screen()

        mouse_pos = pygame.mouse.get_pos()
        if standard_leader_button.collidepoint(mouse_pos):
            stan_modes_color = DARK_GREEN
            smline = True
        else:
            stan_modes_color = GREEN
            smline = False
        if timed_leader_button.collidepoint(mouse_pos):
            timed_modes_color = DARK_GREEN
            tmline = True
        else:
            timed_modes_color = GREEN
            tmline = False
        if ultimate_leader_button.collidepoint(mouse_pos):
            ultim_modes_color = DARK_GREEN
            umline = True
        else:
            ultim_modes_color = GREEN
            umline = False
        pygame.draw.rect(screen, stan_modes_color, standard_leader_button)
        draw_text('Standard Leaderboards', small_font, BLACK, screen, 230, 205, smline)
        pygame.draw.rect(screen, timed_modes_color, timed_leader_button)
        draw_text('Timed Leaderboards', small_font, BLACK, screen, 252, 305, tmline)
        pygame.draw.rect(screen, ultim_modes_color, ultimate_leader_button)
        draw_text('Ultimate Leaderboards', small_font, BLACK, screen, 235, 405, umline)
        pygame.display.flip()

def display_standard_leaderboard():
    screen.fill(LIGHT_GREEN)
    draw_text('Standard Mode Leaderboard', game_font, BLACK, screen, 115, 80)
    c.execute("SELECT name, score FROM standard_scores ORDER BY score ASC LIMIT 5")
    top_scores = c.fetchall()
    y = 200
    for idx, score in enumerate(top_scores):
        draw_text(f'{idx + 1}. {score[0]} - Time: {score[1]} seconds', small_font, BLACK, screen, 115, y)
        y += 50
    pygame.display.flip()
    wait_for_click(display_leaderboards_screen)

def display_timed_leaderboard():
    screen.fill(LIGHT_GREEN)
    draw_text('Timed Mode Leaderboard', game_font, BLACK, screen, 145, 80)
    c.execute("SELECT name, words_typed FROM timed_scores ORDER BY words_typed DESC LIMIT 5")
    top_scores = c.fetchall()
    y = 200
    for idx, score in enumerate(top_scores):
        draw_text(f'{idx + 1}. {score[0]} - Words Unscrambeled: {score[1]} words', small_font, BLACK, screen, 85, y)
        y += 50
    pygame.display.flip()
    wait_for_click(display_leaderboards_screen)

def display_ultimate_leaderboard():
    screen.fill(LIGHT_GREEN)
    draw_text('Ultimate Mode Leaderboard', game_font, BLACK, screen, 115, 80)
    c.execute("SELECT name, words_typed FROM ultimate_scores ORDER BY words_typed DESC LIMIT 7")
    top_scores = c.fetchall()
    y = 200
    for idx, score in enumerate(top_scores):
        draw_text(f'{idx + 1}. {score[0]} - Words Unscrambeled: {score[1]} words', small_font, BLACK, screen, 85, y)
        y += 50
    pygame.display.flip()
    wait_for_click(display_leaderboards_screen)

def wait_for_click(callback):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                callback()

if __name__ == "__main__":
    play()