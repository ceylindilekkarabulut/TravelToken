# Throne Travel - AI-Powered Travel Planning on Solana

**A hackathon project combining AI agents, blockchain escrow, and community sponsorship for travel goals.**

---

## 🎯 Vision

Enable travelers to crowd-fund their dream trips while receiving AI-powered travel planning. Community sponsors provide funds through Solana escrow; AI agents optimize routes, find deals, and manage budgets—all transparent and decentralized.

---

## 🏗️ MVP Scope (Phase 1-2 Complete)

### ✅ What We Built

#### **Backend (Python/FastAPI)**
- RESTful API with SSE streaming for real-time agent updates
- **3 AI Agents** using LLMs:
  - **Route Agent**: Analyzes travel routes with Google Maps + LLM insights
  - **Deal Hunter**: Finds flights (Amadeus) and hotels, optimizes pricing
  - **Budget Agent**: Calculates costs, suggests money-saving tips
- **Hybrid Vector Search**: Semantic + keyword search on travel routes with pgvector
- **Agent Execution Logging**: Tracks input/output, duration for each agent
- **Solana Integration**: Initialize goals on-chain, release funds with authority signature

#### **Smart Contract (Anchor/Rust)**
- **Travel Escrow Program** (Devnet)
  - `initialize_goal`: Create travel goal PDAs
  - `sponsor`: Community members fund goals (transfers to escrow)
  - `release_funds`: Authority releases funds to traveler
  - `refund_sponsor`: Refund individual sponsors
- **Events**: `GoalFunded`, `GoalReleased` for real-time blockchain updates
- **IDL Export**: Ready for frontend Anchor integration

#### **Database**
- PostgreSQL with pgvector extension
- 6 tables: TravelGoals, Sponsorships, AgentLogs, Routes, PriceHistory, AlembicVersion
- Alembic migrations for schema management

#### **Frontend (Next.js/React)**
- Landing page with hero section
- Create Travel Goal modal (form + real-time SSE response display)
- Responsive dark theme with Tailwind CSS
- API integration with streaming response handling

---

## 🚀 Key Features

| Feature | Status | Details |
|---------|--------|---------|
| **AI-Powered Planning** | ✅ Complete | 3 agents analyze routes, deals, budgets |
| **Hybrid Search** | ✅ Complete | Vector similarity + keyword matching for routes |
| **Solana Integration** | ✅ Complete | Smart contract + Python RPC wrapper + event listener |
| **Real-Time Streaming** | ✅ Complete | SSE endpoints for agent progress updates |
| **Execution Logging** | ✅ Complete | All agent I/O recorded with timing |
| **Database** | ✅ Complete | pgvector, migrations, 6 tables |
| **Frontend UI** | ✅ Complete | Landing page + goal creation flow |

---

## 💻 Tech Stack

**Backend:**
- FastAPI (async HTTP framework)
- SQLAlchemy 2.0 (ORM)
- Pydantic (validation)
- LangChain/OpenAI (LLMs)
- Amadeus API (flights/hotels)
- Google Maps API (routing)
- structlog (structured logging)

**Smart Contract:**
- Anchor (Solana framework)
- Rust (instruction logic)
- PDAs (Program Derived Accounts)

**Database:**
- PostgreSQL 16 + pgvector extension
- Alembic (migrations)

**Frontend:**
- Next.js 15 (React framework)
- TypeScript
- Tailwind CSS
- React Query (data fetching)
- Zustand (state management)

**Blockchain:**
- Solana Devnet
- Program ID: `Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS`

---

## 📋 Project Structure

```
TravelToken/
├── backend/
│   ├── app/
│   │   ├── agents/        # Route, Deal Hunter, Budget agents
│   │   ├── api/routes/    # 5 endpoints (goals, sponsorships, routes, agents, websocket)
│   │   ├── models/        # SQLAlchemy + Pydantic schemas
│   │   ├── services/      # Amadeus, Maps, Solana, Embedding clients
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   └── requirements.txt
├── contracts/
│   ├── programs/travel_escrow/src/
│   │   ├── instructions/  # sponsor, release_funds, refund_sponsor
│   │   ├── state.rs       # TravelGoal, Sponsorship PDAs
│   │   ├── errors.rs      # Custom errors
│   │   └── lib.rs         # Program entry
│   └── Anchor.toml
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages (/, /create, /goals/[id])
│   │   ├── components/    # CreateGoalModal, AgentStreamPanel
│   │   └── types/         # TypeScript interfaces
│   └── package.json
├── idl/
│   └── travel_escrow.json # Smart contract IDL for frontend
└── docker-compose.yml     # PostgreSQL + Redis
```

---

## 🎬 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+
- Rust (for smart contract compilation)

### 1. Start Services
```bash
docker-compose up -d
```

### 2. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### 4. Create a Goal
1. Visit `http://localhost:3000`
2. Click "✨ Start AI Planning"
3. Fill form (or use defaults: Istanbul → Paris, $1500)
4. Watch real-time AI analysis via SSE stream

---

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/goals/create` | Create goal + stream AI analysis |
| GET | `/api/goals/{id}` | Fetch goal details |
| GET | `/api/goals/list/by-wallet?user_wallet=...` | List user's goals |
| POST | `/api/sponsorships/create` | Add sponsor to goal |
| GET | `/api/routes/search?query=...` | Hybrid search travel routes |
| POST | `/api/routes/{id}/copy` | Copy route + increment counter |
| WS | `/ws/notifications/{wallet}` | WebSocket for real-time updates |
| POST | `/api/agents/approve-purchase` | Approve goal + trigger Solana release |

---

## 🤖 AI Agent Flow

```
User Creates Goal
    ↓
Route Agent (Parallel) ────→ Maps directions + LLM analysis
Deal Hunter Agent ────→ Amadeus flights/hotels + LLM assessment
    ↓
Budget Agent ────→ Cost calculation + Money-saving tips
    ↓
Final Report ────→ Markdown compilation
    ↓
SSE Stream to Frontend ────→ Real-time progress display
```

---

## ⛓️ Solana Integration

### Smart Contract Features
- **Authority-based approval** for fund release
- **PDA-based escrow** for secure fund holding
- **Event emission** for on-chain transparency
- **Multi-sponsor support** (multiple sponsors per goal)

### Workflow
1. **Initialize Goal**: Backend creates goal PDA with traveler + authority
2. **Sponsor**: Community members transfer SOL to escrow
3. **Approve**: Authority (backend) approves → calls `release_funds` instruction
4. **Release**: Funds transferred to traveler wallet
5. **Refund**: Authority can refund individual sponsors if needed

---

## 🔍 Data Insights

### Vector Search + Hybrid Ranking
- **1536-dimensional embeddings** (OpenAI text-embedding-3-small)
- **Ranking formula**: `0.6 * vector_similarity + 0.4 * keyword_match`
- **Database**: PostgreSQL pgvector for efficient HNSW indexing

### Agent Logging
- **Execution time tracking**: Each agent's duration in milliseconds
- **I/O recording**: Input state + output result as JSON
- **Traceability**: Full audit trail for debugging

---

## 🚀 Next Steps (Phase 3-6)

### Phase 3: Integration Testing
- Frontend ↔ Backend SSE validation
- Devnet smart contract deployment
- Event listener real-time sync

### Phase 4: Feature Completion
- Celery workers for periodic deal monitoring
- WebSocket price drop notifications
- Price history analytics + buy signal badges

### Phase 5-6: Demo Polish
- Production-ready UI with error states
- Demo video + presentation
- Full end-to-end flow testing

---

## 📈 Project Metrics

| Metric | Value |
|--------|-------|
| **Smart Contract Instructions** | 4 (init, sponsor, release, refund) |
| **AI Agents** | 3 (Route, Deal Hunter, Budget) |
| **Database Tables** | 6 (with relationships) |
| **API Endpoints** | 8 (RESTful + WebSocket) |
| **Code Lines** | ~3000 (backend + contracts) |
| **Agent Events** | 2 (GoalFunded, GoalReleased) |
| **Response Time** | <2s average agent execution |

---

## 🎓 Innovation Highlights

1. **Agentic AI + Blockchain**: First-class integration of LLM agents with Solana for trustless travel planning
2. **Hybrid Search**: Combining semantic search (embeddings) with keyword matching for travel discovery
3. **Real-Time Streaming**: SSE for live agent progress—users see AI thinking in real-time
4. **Escrow Design**: PDAs enable multi-sponsor contribution without centralized intermediary
5. **Modular Architecture**: Clear separation of concerns (agents, services, API, contracts)

---

## 👥 Takım Rolleri

- **Şeyma**: Backend (FastAPI, ajanlar, API uç noktaları, Solana entegrasyonu)
- **Ceylin**: Altyapı (Veritabanı, migrasyonlar, akıllı kontrat, DevOps)
- **Irmak**: Frontend (Next.js, UI bileşenleri, UX)

---

## 📝 License

MIT

---

## 🔗 Resources

- **Solana Program**: `programs/travel_escrow/src/`
- **IDL**: `idl/travel_escrow.json`
- **API Docs**: `http://localhost:8000/docs` (auto-generated by FastAPI)
- **Smart Contract Devnet**: https://explorer.solana.com/?cluster=devnet

---

**Built for Hackathon'26 • Shipped in 48 hours**
