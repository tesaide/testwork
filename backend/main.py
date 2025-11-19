from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import database
import game_logic

app = FastAPI()

# Налаштування CORS (дозвіл для фронта)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В тут потрібен домен продакшена
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данних для валідації запрос/відповідь
class BetRequest(BaseModel):
    bet: int

class InitResponse(BaseModel):
    balance: float

class RollResponse(BaseModel):
    dice: list[int]
    combination: str
    win_amount: int
    balance: float

@app.post("/init", response_model=InitResponse)
def init_game():
    """
    Ініціалізація гри. Якщо немає транзакцій, нараховує 100 монет.
    """
    if not database.has_transactions():
        database.add_transaction(100, "Init")
    return {"balance": database.get_balance()}

@app.get("/balance")
def get_current_balance():
    """Повертає баланс."""
    return {"balance": database.get_balance()}

@app.post("/roll", response_model=RollResponse)
def make_roll(request: BetRequest):
    """
    Основа дії:
    1. Списує ставку.
    2. Кидає кубики.
    3. Рахує виграш.
    4. Нараховує виграш якщо є.
    5. Повертає результат.
    """
    bet = request.bet
    current_balance = database.get_balance()

    # Валидація ставки
    if bet <= 0:
        raise HTTPException(status_code=400, detail="Ставка має бути позитивною")
    if bet > current_balance:
        raise HTTPException(status_code=400, detail="Недостатньо коштів")

    
    # "Якщо я ставлю 30, то API має створити {value: -30, type: 'Bet'}"
    database.add_transaction(-bet, "Bet")

    # 2. Кидаєм кубики (RNG) 
    dice = game_logic.roll_dice()

    # 3. Визначаємо комбінацію та виграш
    combo_name, multiplier = game_logic.check_combination(dice)
    
    win_amount = bet * multiplier

    # 4. Якщо є виграш, записуємо транзакцію
    if win_amount > 0:
        database.add_transaction(win_amount, "Win")

    # 5. Отримуємо актуальний баланс
    new_balance = database.get_balance()

    return {
        "dice": dice,
        "combination": combo_name,
        "win_amount": win_amount,
        "balance": new_balance
    }

if __name__ == "__main__":
    import uvicorn
    # Запуск сервера на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)