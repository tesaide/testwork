from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
import game_logic

app = FastAPI()

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models for request/response validation
class BetRequest(BaseModel):
    bet: int

class InitResponse(BaseModel):
    balance: float

class RollResponse(BaseModel):
    dice: list[int]
    combination: str
    win_amount: float
    balance: float

@app.post("/init", response_model=InitResponse)
def init_game():
    """
    Initialize the game. If no transactions exist, add 100 coins.
    """
    if not database.has_transactions():
        database.add_transaction(100, "Init")
    return {"balance": database.get_balance()}

@app.get("/balance")
def get_current_balance():
    """Returns current balance."""
    return {"balance": database.get_balance()}

@app.post("/roll", response_model=RollResponse)
def make_roll(request: BetRequest):
    """
    Main game action:
    1. Deduct bet.
    2. Roll dice.
    3. Calculate win.
    4. Add win amount if any.
    5. Return result.
    """
    bet = request.bet
    current_balance = database.get_balance()

    # Validate bet
    if bet <= 0:
        raise HTTPException(status_code=400, detail="Bet must be positive")
    if bet > current_balance:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # 1. Deduct bet (create negative transaction)
    # "If I bet 30, API must create {value: -30, type: 'Bet'}"
    database.add_transaction(-bet, "Bet")

    # 2. Roll dice (RNG)
    dice = game_logic.roll_dice()

    # 3. Determine combination and win amount
    combo_name, multiplier = game_logic.check_combination(dice)
    
    win_amount = bet * multiplier

    # 4. If player wins, record the transaction
    if win_amount > 0:
        database.add_transaction(win_amount, "Win")

    # 5. Get updated balance
    new_balance = database.get_balance()

    return {
        "dice": dice,
        "combination": combo_name,
        "win_amount": win_amount,
        "balance": new_balance
    }

if __name__ == "__main__":
    import uvicorn
    # Start server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)