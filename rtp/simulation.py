import sys
import os
import random
from collections import Counter

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.join(current_dir, '..', 'backend')
sys.path.append(backend_path)

try:
    from game_logic import roll_dice
except ImportError:
    print("Не знайдено файл game_logic.py")
    print(f"Переконайтеся, що у папці testwork/backend є файл game_logic.py")
    sys.exit(1)

# --- Налаштування симуляції ---
SIMULATIONS_COUNT = 1_000_000  # кількість ігор
BET_AMOUNT = 10 


ORIGINAL_ODDS = {
    "Three Pairs": 4,
    "Yahtzee": 3,
    "4+2": 2,
    "Pair": 1
}

NEW_ODDS = {
    "Three Pairs": 4.0,  # Стандартний x4 (це рідкість, не страшно)
    "Yahtzee": 20.0,     
    "4+2": 3.0,          # Трохи вище стандарту
    "Pair": 0.82         # Знижуємо найчастішу виплату
}


def check_combination_with_odds(dice, odds_table):
    """
    Логіка перевірки виграшу з таблицею коефіцієнтів, що настроюється.
    """
    counts = Counter(dice)
    values = list(counts.values())
    
    # Перевіряємо від найціннішої до простої
    if values.count(2) == 3:
        return odds_table["Three Pairs"]
    if 6 in values:
        return odds_table["Yahtzee"]
    if 4 in values and 2 in values:
        return odds_table["4+2"]
    if any(count >= 2 for count in values):
        return odds_table["Pair"]
    
    return 0 # Немає виграшу

def run_simulation(iterations, odds_table, title):
    print(f"\n--- {title} ---")
    print(f"Запуск симуляції на {iterations} ігор...")
    
    total_bet = 0
    total_win = 0
    
    for _ in range(iterations):
        total_bet += BET_AMOUNT
        dice = roll_dice() # Генеруємо випадковий кидок
        multiplier = check_combination_with_odds(dice, odds_table)
        
        win = BET_AMOUNT * multiplier
        total_win += win

    rtp = (total_win / total_bet) * 100
    
    print(f"Всього ставок: {total_bet}")
    print(f"Всього перемог: {total_win}")
    print(f"Фінальний RTP: {rtp:.2f}%")
    
    if 94 < rtp < 96:
        print("Показник в нормі (~95%)")
    elif rtp < 50:
        print("Алгоритм занадто суворий (Task #1)")
    
if __name__ == "__main__":
    # Завдання 1: Перевірити поточні налаштування
    run_simulation(SIMULATIONS_COUNT, ORIGINAL_ODDS, "Завдання 1: Базові налаштування")
    
    # Завдання 2: Підібрати RTP ~95%
    run_simulation(SIMULATIONS_COUNT, NEW_ODDS, "Завдання 2: Оптимізовані налаштування")