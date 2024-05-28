import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Настройки окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Игра 21")

# Шрифт для отображения текста
font = pygame.font.SysFont(None, 36)

# Класс для представления карты
class Card:
    def __init__(self, value):
        self.value = value

    def draw(self, x, y):
        pygame.draw.rect(screen, WHITE, (x, y, 50, 80))
        card_text = font.render(str(self.value), True, BLACK)
        screen.blit(card_text, (x + 10, y + 10))

# Составление колоды карт
deck = []
for i in range(1, 11):
    deck.extend([i]*4)

player_hand = []
dealer_hand = []

# Функция для подсчета очков
def calculate_score(hand):
    score = sum(card.value for card in hand)
    return min(score, 21)

# Раздача карт игроку и дилеру
for i in range(2):
    player_hand.append(Card(random.choice(deck)))
    dealer_hand.append(Card(random.choice(deck)))

# Основной игровой цикл
running = True
player_turn = True
dealer_turn = False

while running:
    screen.fill(BLACK)

    # Отрисовка карт игрока
    for i, card in enumerate(player_hand):
        card.draw(100 + i*60, 300)

    # Отрисовка карт дилера
    for i, card in enumerate(dealer_hand):
        card.draw(100 + i*60, 100)

    # Отображение очков
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    player_score_text = font.render(f"Очки игрока: {player_score}", True, WHITE)
    dealer_score_text = font.render(f"Очки дилера: {dealer_score}", True, WHITE)
    screen.blit(player_score_text, (10, 10))
    screen.blit(dealer_score_text, (10, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif player_turn and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:  # Hit
                player_hand.append(Card(random.choice(deck)))
                pygame.display.update()  # Обновление отображения после добавления карты
            elif event.key == pygame.K_s:  # Stand
                player_turn = False
                dealer_turn = True

    if player_turn:
        continue

    # Логика дилера
    while dealer_score < 17:
        dealer_hand.append(Card(random.choice(deck)))
        dealer_score = calculate_score(dealer_hand)

    # Определение победителя
    if dealer_score > 21 or player_score > dealer_score:
        result_text = font.render("Игрок победил!", True, WHITE)
    elif player_score == dealer_score:
        result_text = font.render("Ничья!", True, WHITE)
    else:
        result_text = font.render("Дилер победил!", True, WHITE)
    screen.blit(result_text, (10, 100))

    # Обновление отображения карт после каждого хода
    for i, card in enumerate(player_hand):
        card.draw(100 + i*60, 300)
    for i, card in enumerate(dealer_hand):
        card.draw(100 + i*60, 100)

    pygame.display.flip()

pygame.quit()
