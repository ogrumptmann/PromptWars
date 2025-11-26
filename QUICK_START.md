# Prompt Wars - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Clone & Checkout
```bash
git clone https://github.com/ogrumptmann/PromptWars.git
cd PromptWars
git checkout feature/phase-2-core-game-loop
```

### 2. Create `.env` File
```bash
# Copy this into .env file in project root
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4
```

### 3. Start Docker
```bash
docker-compose up -d
```

### 4. Open Browser
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:3001/docs

---

## 🎮 Test the Game

1. Open http://localhost:5173
2. Click 1-3 cards to select them (they'll highlight yellow)
3. Write a creative prompt in the text area
4. Click "CAST" button
5. Watch the battle result in the Battle Log!

---

## 🧪 Run Tests

```bash
# Backend tests (117 tests, 76% coverage)
docker-compose exec backend pytest -v

# Frontend tests (74 tests, 56 passing)
docker-compose exec frontend npm test
```

---

## 📋 What's Working

✅ Card system (20 cards: Elements, Actions, Materials)  
✅ AI Judge (evaluates prompts and determines winners)  
✅ Battle system (damage calculation, HP tracking)  
✅ Mobile-first UI (Header, Arena, Cards, Input)  
✅ State management (Zustand + Redis)  

---

## 🐛 Known Issues

⚠️ **18 frontend tests failing** - Need updates for new UI  
⚠️ **HP subtraction** - May need testing/debugging  
⚠️ **Timer static** - Shows 45s but doesn't count down  

---

## 🔜 Next Task: WebSocket Game Protocol (Task 2.6)

Implement real-time multiplayer:
- JOIN_ROOM event
- TURN_START event  
- TURN_RESULT event
- GAME_OVER event

See `STATUS.md` for full details.

---

## 🆘 Troubleshooting

**Docker not starting?**
```bash
# Check Docker Desktop is running
docker ps

# Rebuild containers if needed
docker-compose down
docker-compose build
docker-compose up -d
```

**Frontend not loading?**
```bash
# Check logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

**Backend errors?**
```bash
# Check logs
docker-compose logs backend

# Verify .env file has OPENAI_API_KEY
cat .env
```

---

## 📚 More Info

- Full status: `STATUS.md`
- Design doc: `docs/MASTER_DESIGN.md`
- Repository: https://github.com/ogrumptmann/PromptWars

**Happy coding!** 🎉

