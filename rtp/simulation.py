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
    print("game_logic.py not found")
    print(f"Ensure that testwork/backend contains game_logic.py")
    sys.exit(1)

# --- Simulation Settings ---
SIMULATIONS_COUNT = 1_000_000  # number of games
BET_AMOUNT = 10 

ORIGINAL_ODDS = {
    "Three Pairs": 4,
    "Yahtzee": 3,
    "4+2": 2,
    "Pair": 1
}

NEW_ODDS = {
    "Three Pairs": 4.0,  # Standard x4 (rare, so okay)
    "Yahtzee": 20.0,     
    "4+2": 3.0,          # Slightly higher than standard
    "Pair": 0.82         # Lowering the most frequent payout to balance RTP
}


def check_combination_with_odds(dice, odds_table):
    """
    Logic to check win using a customizable odds table.
    """
    counts = Counter(dice)
    values = list(counts.values())
    
    # Check from highest to lowest value
    if values.count(2) == 3:
        return odds_table["Three Pairs"]
    if 6 in values:
        return odds_table["Yahtzee"]
    if 4 in values and 2 in values:
        return odds_table["4+2"]
    if any(count >= 2 for count in values):
        return odds_table["Pair"]
    
    return 0 # No win

def run_simulation(iterations, odds_table, title):
    print(f"\n--- {title} ---")
    print(f"Running simulation for {iterations} games...")
    
    total_bet = 0
    total_win = 0
    
    for _ in range(iterations):
        total_bet += BET_AMOUNT
        dice = roll_dice() # Generate random roll
        multiplier = check_combination_with_odds(dice, odds_table)
        
        win = BET_AMOUNT * multiplier
        total_win += win

    rtp = (total_win / total_bet) * 100
    
    print(f"Total Bets: {total_bet}")
    print(f"Total Wins: {total_win}")
    print(f"Final RTP: {rtp:.2f}%")
    
    if 94 < rtp < 96:
        print("RTP is ideal (~95%)")
    elif rtp < 50:
        print("Algorithm is too strict (Task #1)")
    
if __name__ == "__main__":
    # Task 1: Check original settings
    run_simulation(SIMULATIONS_COUNT, ORIGINAL_ODDS, "Task 1: Original Settings")
    
    # Task 2: Find RTP ~95%
    run_simulation(SIMULATIONS_COUNT, NEW_ODDS, "Task 2: Optimized Settings")