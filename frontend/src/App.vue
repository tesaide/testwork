<script setup>
import { ref, onMounted } from 'vue'

// Game state variables
const balance = ref(0)
const betAmount = ref(30)
const dice = ref([1, 1, 1, 1, 1, 1])
const isRolling = ref(false)
const message = ref('')

// Backend URL
const API_URL = 'http://localhost:8000'

// Initialize game and fetch balance
const initGame = async () => {
  try {
    const res = await fetch(`${API_URL}/init`, { method: 'POST' })
    if (!res.ok) throw new Error('Init failed')
    const data = await res.json()
    balance.value = data.balance
  } catch (e) {
    console.error(e)
    message.value = "Error: Cannot connect to server"
  }
}

// Handle roll button click
const makeRoll = async () => {
  if (isRolling.value) return
  
  // Check if user has enough money
  if (betAmount.value > balance.value) {
    message.value = "Insufficient funds!"
    return
  }
  
  isRolling.value = true
  message.value = "Rolling..." 
  
  try {
    const res = await fetch(`${API_URL}/roll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bet: betAmount.value })
    })
    
    if (!res.ok) {
      const errData = await res.json()
      throw new Error(errData.detail || 'Server Error')
    }

    const data = await res.json()
    
    // Delay updates for animation effect
    setTimeout(() => {
      dice.value = data.dice
      balance.value = data.balance
      
      if (data.win_amount > 0) {
        message.value = `WIN! ${data.combination} (+${data.win_amount})`
      } else {
        message.value = `Lose. ${data.combination}`
      }
      
      isRolling.value = false
    }, 600)
    
  } catch (e) {
    console.error(e)
    isRolling.value = false
    message.value = `Error: ${e.message}`
  }
}

onMounted(() => {
  initGame()
})
</script>

<template>
  <div class="game-container">
    
    <div class="card dice-area">
      <h2>Dice</h2>
      <div class="dice-row">
        <div v-for="(num, i) in dice" :key="i" class="die">
          {{ isRolling ? '?' : num }}
        </div>
      </div>
    </div>

    <div class="controls">
      
      <div class="card prices">
        <h3>Prices</h3>
        <div class="row"><span>Pair</span> <b>x0.82</b></div>
        <div class="row"><span>4+2</span> <b class="red">x3.0</b></div>
        <div class="row"><span>Yahtzee</span> <b>x20.0</b></div>
        <div class="row"><span>Three Pairs</span> <b>x4.0</b></div>
      </div>

      <div class="right-panel">
        
        <div class="card bet-box">
          <h3>Bet</h3>
          <div class="bet-input-row">
            <input type="number" v-model="betAmount" class="bet-input" min="1">
            <button 
              @click="makeRoll" 
              :disabled="isRolling" 
              class="roll-btn"
            >
              ROLL
            </button>
          </div>
        </div>

        <div class="balance-box">
          <p>Your balance</p>
          <div class="balance-num">{{ Math.floor(balance * 100) / 100 }}</div>
          <div class="msg">{{ message }}</div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
.game-container {
  max-width: 600px;
  margin: 40px auto;
  font-family: Arial, sans-serif;
  color: #333;
}

.card {
  background: #fff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 20px;
}

h2, h3 {
  margin: 0 0 15px 0;
  text-align: center;
}

.dice-row {
  display: flex;
  justify-content: center;
  gap: 10px;
}
.die {
  width: 50px;
  height: 50px;
  border: 2px solid #333;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  background-color: #fff;
}

.controls {
  display: flex;
  gap: 20px;
}

.prices {
  flex: 1;
}
.row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px solid #eee;
  font-size: 16px;
}
.red {
  color: #e74c3c;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bet-box {
  text-align: center;
}
.bet-input-row {
  display: flex;
  gap: 10px;
  justify-content: center;
}
.bet-input {
  width: 70px;
  font-size: 18px;
  text-align: center;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.roll-btn {
  background: #ff8a80;
  border: 1px solid #333;
  padding: 5px 20px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 4px;
  text-transform: uppercase;
  transition: background 0.2s;
}
.roll-btn:hover {
  background: #ff5252;
}
.roll-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.balance-box {
  text-align: center;
  margin-top: 5px;
}
.balance-num {
  font-size: 36px;
  font-weight: bold;
}
.msg {
  min-height: 20px;
  color: #666;
  font-size: 14px;
  margin-top: 5px;
}
</style>