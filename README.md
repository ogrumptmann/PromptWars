# ⚔️ Prompt Wars

An AI-powered text-based strategy game where players battle using creative prompts judged by Large Language Models.

## 🎮 Game Concept

Prompt Wars is a simultaneous turn-based combat game where:
- Players select constraint cards (Fire, Ice, Shield, etc.)
- Write creative prompts that match their card's theme
- An AI referee judges validity and determines battle outcomes
- Strategic thinking meets creative writing in epic duels

## 🏗️ Architecture

### Tech Stack
- **Frontend**: React 19 + Vite + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI
- **Database**: Redis (game state + leaderboards)
- **AI**: Configurable LLM providers (OpenAI, Gemini, Ollama)
- **Infrastructure**: Docker + Docker Compose

### Project Structure
```
/prompt-wars
  /backend          # FastAPI Python backend
    /app
      /api          # REST & WebSocket endpoints
      /core         # Configuration
      /logic        # Game rules & Elo calculation
      /models       # Pydantic schemas
      /providers    # LLM adapters
      /services     # Business logic
      /data         # Card registry
  /frontend         # React + Vite frontend
    /src
      /components   # React components
      /hooks        # Custom hooks
      /store        # Zustand state management
  /Documentation    # Design documents
```

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PromptWars
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Start all services**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:3001
   - API Docs: http://localhost:3001/docs

### Development

All services run in Docker with hot-reload enabled:
- Frontend changes auto-refresh in browser
- Backend changes auto-restart FastAPI server
- No local Python/Node installation required

## 📋 Development Phases

- [x] **Phase 1**: Infrastructure Setup (Docker, FastAPI, React, Redis)
- [ ] **Phase 2**: Core Game Loop (AI Judge, Cards, WebSocket)
- [ ] **Phase 3**: Visual Layer (PixiJS particle effects)
- [ ] **Phase 4**: Matchmaking & Progression (Elo, Leaderboards)
- [ ] **Phase 5**: Polish & Deployment (Azure Container Apps)

## 🎴 Game Features

### Card Types
- **Elements** (10): Fire, Ice, Water, Earth, Wind, Lightning, Shadow, Light, Sound, Poison
- **Actions** (6): Shield, Melee, Range, Trap, Heal, Haste
- **Materials** (4): Iron, Nature, Crystal, Cyber

### Game Mechanics
- Simultaneous turn-based combat (We-Go system)
- AI-powered prompt validation
- Environment effects that change battle conditions
- Elo rating system for competitive ranking
- Real-time matchmaking

## 📚 Documentation

See `/Documentation` folder for:
- Master Design Document
- API specifications
- Game mechanics details
- Implementation roadmap

## 🛠️ Useful Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up --build

# Access backend shell
docker exec -it promptwars-backend bash

# Access frontend shell
docker exec -it promptwars-frontend sh
```

## 🧪 Testing

### Running Tests

**All tests (recommended before committing):**
```bash
# Windows
.\run-tests.ps1

# Linux/Mac
./run-tests.sh
```

**Backend tests only:**
```bash
docker-compose exec backend python -m pytest -v
```

**Frontend tests only:**
```bash
docker-compose exec frontend npm test -- --run
```

### Test Coverage

- **Backend**: 50% minimum coverage required (pytest + pytest-cov)
- **Frontend**: Vitest with React Testing Library
- **CI/CD**: GitHub Actions runs all tests on push/PR
- Coverage will increase as more features are implemented in Phase 2+

### Test Structure

**Backend** (`backend/tests/`):
- `test_health.py` - Health check endpoint tests
- `test_redis_service.py` - Redis operations tests
- `test_websocket.py` - WebSocket connection manager tests

**Frontend** (`frontend/src/`):
- `App.test.jsx` - Main app component tests
- `hooks/useWebSocket.test.js` - WebSocket hook tests

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

This is a learning project. Contributions welcome!

---

**Current Status**: Phase 1 Complete - Infrastructure Ready ✅

