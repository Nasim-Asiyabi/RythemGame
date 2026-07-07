
```markdown
# 🎵 Rhythm Master

![Pygame](https://img.shields.io/badge/Pygame-2.0+-green)
![Python](https://img.shields.io/badge/Python-3.6+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

A **4-lane rhythm game** built with Python and Pygame where you test your reflexes by hitting notes in time with the rhythm.

## 🎮 Gameplay Preview

![Gameplay Screenshot](https://via.placeholder.com/810x620/1a1a2e/ffffff?text=Rhythm+Master+Preview)

- **4 lanes** with notes falling from the top
- **Hit notes** by pressing `D`, `F`, `J`, `K` at the perfect time
- **Build combos** and **climb the leaderboard**!

## ✨ Features

### Core Mechanics
- 🎯 **Precision Scoring** – Perfect (+20), Good (+10), OK (+5)
- 🔥 **Combo System** – Visual color changes at 10, 25, and 50 combo
- 📈 **Dynamic Difficulty** – Speed increases with your score (up to 12x)
- ❤️ **Health System** – Miss notes and lose health
- 🏆 **High Score Tracking** – Persistent across sessions

### Visual Design
- 🎨 **Color-coded feedback** – Green (Perfect), Yellow (Good), Red (Miss)
- 💜 **Combo colors** – White → Green → Yellow → Purple
- 📊 **Real-time HUD** – Score, Combo, Speed, Best Score, Health Bar

### User Interface
- 🏠 **Main Menu** – High score display and start prompt
- ⚔️ **Game Over Screen** – Detailed stats (Perfect/Good/OK/Miss)
- 🔄 **Restart** – Press `R` to try again

## 🎯 How to Play

### Controls
| Action | Key |
|--------|-----|
| Lane 1 (Left) | `D` |
| Lane 2 | `F` |
| Lane 3 | `J` |
| Lane 4 (Right) | `K` |
| Start Game | `Enter` |
| Retry | `R` |
| Quit | `Escape` |

### Scoring System
| Hit Type | Points | Health |
|----------|--------|--------|
| **PERFECT** | +20 | +2 |
| **GOOD** | +10 | +1 |
| **OK** | +5 | +0 |
| **MISS** | 0 | -5 to -10 |

### Combo Bonuses
- 🎯 **10 combo** → Green text
- ⭐ **25 combo** → Yellow text  
- 💜 **50+ combo** → Purple text

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- Pygame library

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/Nasim-Asiyabi/rhythm-master.git
cd rhythm-master

# 2. Install Pygame
pip install pygame

# 3. Run the game
python rythemgame.py
