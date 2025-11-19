import random
from collections import Counter
from typing import List, Tuple

# Оновлений коефіцієнт (RTP ~95.31%)
ODDS = {
    "Three Pairs": 4.0,
    "Yahtzee": 20.0,    # Джекпот
    "4+2": 3.0,
    "Pair": 0.82        
}

def roll_dice() -> List[int]:
    """Генерація 6 випадкових чисел  1 - 6."""
    
    return [random.randint(1, 6) for _ in range(6)]

def check_combination(dice: List[int]) -> Tuple[str, int]:
    """
    Визначає виграшний прибуток та повертає (Назва, Множитель).
    Повертає('Інше', 0), якщо комбінацій немає.
    """
    counts = Counter(dice)
    values = list(counts.values())
    
    if values.count(2) == 3:
        return "Three Pairs", ODDS["Three Pairs"]

    if 6 in values:
        return "Yahtzee", ODDS["Yahtzee"]

    if 4 in values and 2 in values:
        return "4+2", ODDS["4+2"]

    if any(count >= 2 for count in values):
        return "Pair", ODDS["Pair"]

    return "Other", 0