

# Yahtzee Game 


Stack: **Vue 3 (Vite)** + **Python (FastAPI, SQLite)**.


## Project Structure


- **backend/**: Python API server + Game Logic + Database.

- **frontend/**: Vue.js client application.

- **rtp/**: Simulation scripts for mathematical analysis.


---


## How to Run


You will need two terminal windows (one for the server, one for the client).


### 1. Start Backend (Server)

```bash

# 1. Create and activate virtual environment

python3 -m venv venv

source venv/bin/activate

# For Windows use: venv\Scripts\activate


# 2. Install dependencies and run server

cd backend

pip install -r requirements.txt

python main.py

# Server will start at [http://0.0.0.0:8000](http://0.0.0.0:8000)

```

### 2\. Start Frontend (UI)


Open a new terminal tab and run:


```bash

cd frontend

npm install

npm run dev

# App will start at http://localhost:5173

```


-----


## Math Analysis & Deliverables


As per "Part 2. Analysis", a simulation of **1,000,000 games** was performed to calculate the Return To Player (RTP).


### Task \#1: Current RTP


Using the original odds from the task description (Pair x1, 4+2 x2, etc.):


  - **Calculated RTP:** \~111%

  - **Conclusion:** The math was broken; the game would lose balance in the long run because the "Pair" combination appears too frequently (\~97% of the time) with a x1 return.


### Task #2: Adjusted Odds (Target ~95%)

To achieve a stable **95% RTP**, the coefficients were optimized. The most critical change was lowering the "Pair" multiplier below 1.

| Combination | Original Odds | New Odds (95% RTP) |
|:---|:---:|:---:|
| **Pair** | x1 | **x0.82** |
| **4+2** | x2 | **x3.0** |
| **Yahtzee** | x3 | **x20.0** |
| **Three Pairs**| x4 | **x4.0** |

**Final Verified RTP:** ~95.3%


-----


## Verification Steps


You can verify the implementation details as follows:


1.  **Verify Math & RTP:**

    Run the simulation script to see both original (111%) and optimized (95%) RTP results:


    ```bash

    python3 rtp/simulation.py

    ```


2.  **Verify Database Persistence:**

    The app uses SQLite. After playing a few rounds, you can inspect `backend/game.db` to see that transactions (`Bet` and `Win`) are correctly saved in the `transactions` table.


3.  **Verify Cleanliness:**

    The repository includes a `.gitignore` file to prevent `node_modules`, `venv`, and other temporary files from cluttering the source code.


<!-- end list -->
