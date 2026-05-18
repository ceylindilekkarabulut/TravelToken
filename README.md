# Throne-Travel — Hackathon'26 Görev Takibi

> Format: `[ ] (Adım X) [DEV] Görev açıklaması`

## Faz 1: Setup & Foundation (Saat 0-6)

### Repo & Infra
- [X] (1) [NAHIDE] Repo oluştur, klasör yapısını scaffold et, ilk commit
- [ ] (1) [NAHIDE] `.env.example` dosyalarını doldur (backend + frontend)
- [ ] (1) [NAHIDE] `docker-compose.yml` ile Postgres+Redis ayağa kaldır
- [ ] (1) [NAHIDE] `pgvector` extension'ı migration'a ekle
- [ ] (1) [NAHIDE] GitHub remote bağla, branch protection ayarla

### Backend Bootstrap
- [ ] (1) [ŞEYMA] FastAPI iskelet (`main.py` + `/health` endpoint)
- [ ] (1) [ŞEYMA] Pydantic settings (`config.py`) — env var okuma
- [ ] (1) [ŞEYMA] `structlog` logger setup
- [ ] (1) [ŞEYMA] `state.py` — TravelState ve agent I/O Pydantic şemaları
- [ ] (1) [ŞEYMA] OpenAI API key test çağrısı (LLM client)
- [ ] (1) [ŞEYMA] Amadeus client wrapper iskeleti + auth test

### Database
- [ ] (1) [NAHIDE] SQLAlchemy 2.0 modelleri (`db.py` — 7 tablo)
- [ ] (1) [NAHIDE] Alembic init, ilk migration, `CREATE EXTENSION vector` ekle
- [ ] (1) [NAHIDE] Migration'ı çalıştır, tabloları doğrula

### Smart Contract
- [ ] (1) [NAHIDE] Anchor init, Devnet keypair oluştur, faucet'tan SOL al
- [ ] (1) [NAHIDE] `state.rs` — TravelGoal + Sponsorship PDA struct'ları
- [ ] (1) [NAHIDE] `errors.rs` — custom error enum'ları
- [ ] (1) [NAHIDE] `initialize_goal` instruction'ı + lokal test

### Frontend Bootstrap
- [ ] (1) [BEYZANUR] Next.js + Tailwind + shadcn/ui init
- [ ] (1) [BEYZANUR] `layout.tsx` + dark mode default
- [ ] (1) [BEYZANUR] `Navbar.tsx` + logo + arama input
- [ ] (1) [BEYZANUR] Solana Wallet Adapter context provider
- [ ] (1) [BEYZANUR] `WalletButton.tsx` (Phantom connect/disconnect)
- [ ] (1) [BEYZANUR] Tasarım tokenları (renkler, font) `tailwind.config.ts`'e

## Faz 2: Core Build (Saat 6-20)

### Backend API
- [ ] (2) [ŞEYMA] `POST /api/goals/create` endpoint (SSE stream döner)
- [ ] (2) [ŞEYMA] `GET /api/goals/{id}` endpoint
- [ ] (2) [ŞEYMA] `GET /api/goals/list?user_wallet=...` endpoint
- [ ] (2) [ŞEYMA] `POST /api/sponsorships/create` endpoint
- [ ] (2) [ŞEYMA] `GET /api/routes/search` endpoint (hybrid search)
- [ ] (2) [ŞEYMA] `POST /api/routes/{id}/copy` endpoint
- [ ] (2) [ŞEYMA] `WS /ws/notifications/{wallet}` endpoint
- [ ] (2) [ŞEYMA] `POST /api/agents/approve-purchase` endpoint

### AI Agents
- [ ] (2) [ŞEYMA] Rota Ajanı — Google Maps Directions + LLM insight
- [ ] (2) [ŞEYMA] Rota Ajanı — Pydantic validation + retry
- [ ] (2) [ŞEYMA] Fırsat Avcısı — Amadeus Flight Offers entegrasyonu
- [ ] (2) [ŞEYMA] Fırsat Avcısı — Amadeus Hotel Search entegrasyonu
- [ ] (2) [ŞEYMA] Fırsat Avcısı — Itinerary Price Metrics + LLM yorumlama
- [ ] (2) [ŞEYMA] Fırsat Avcısı — Redis cache layer (TTL 1 saat)
- [ ] (2) [ŞEYMA] Bütçe Ajanı — deterministik hesap + country food lookup
- [ ] (2) [ŞEYMA] Bütçe Ajanı — LLM saving tips üretimi
- [ ] (2) [ŞEYMA] Master Orchestrator — LangGraph StateGraph
- [ ] (2) [ŞEYMA] ROUTE + DEAL paralel execution (`asyncio.gather`)
- [ ] (2) [ŞEYMA] Final report markdown compile (orchestrator prompt)
- [ ] (2) [ŞEYMA] Agent_logs tablosuna her ajan I/O kaydı

### Vector Search
- [ ] (2) [NAHIDE] `embedding_service.py` — text-embedding-3-small wrapper
- [ ] (2) [NAHIDE] Hybrid search query (vector + filter + re-rank)
- [ ] (2) [NAHIDE] HNSW index optimize parametreleri

### SSE Streaming
- [ ] (2) [ŞEYMA] LangGraph stream → SSE event mapping
- [ ] (2) [ŞEYMA] SSE event tipleri (agent_start, complete, error, done)

### Smart Contract
- [ ] (2) [NAHIDE] `sponsor` instruction + Sponsorship PDA oluşturma
- [ ] (2) [NAHIDE] `release_funds` instruction (backend authority)
- [ ] (2) [NAHIDE] `refund_sponsor` instruction
- [ ] (2) [NAHIDE] `emit!` events (GoalFunded, GoalReleased)
- [ ] (2) [NAHIDE] Anchor IDL export (frontend için)
- [ ] (2) [NAHIDE] Devnet deploy, program ID kayıt

### Solana Service (Python)
- [ ] (2) [NAHIDE] `solana_service.py` — RPC wrapper
- [ ] (2) [NAHIDE] `initialize_goal` backend'den çağırma
- [ ] (2) [NAHIDE] `release_funds` backend'den çağırma
- [ ] (2) [NAHIDE] Solana event listener (WebSocket subscription)

### Frontend Pages
- [ ] (2) [BEYZANUR] Landing page (`/`) — trending goals feed
- [ ] (2) [BEYZANUR] `GoalCard.tsx` — feed item component
- [ ] (2) [BEYZANUR] `GoalProgress.tsx` — progress bar + sponsor count
- [ ] (2) [BEYZANUR] `/create` page — form (react-hook-form + zod)
- [ ] (2) [BEYZANUR] **`AgentStreamPanel.tsx`** — SSE consume (KRİTİK)
- [ ] (2) [BEYZANUR] Framer Motion animasyonları (agent kartları)
- [ ] (2) [BEYZANUR] `/goals/[id]` page — tabs (Plan/Sponsorlar/Fiyat)
- [ ] (2) [BEYZANUR] `SponsorModal.tsx` — Phantom popup tetikleme
- [ ] (2) [BEYZANUR] `FinalReportRenderer.tsx` — markdown render
- [ ] (2) [BEYZANUR] `RouteMap.tsx` — Mapbox component
- [ ] (2) [BEYZANUR] `/routes/search` page — search bar + filters
- [ ] (2) [BEYZANUR] `RouteResultCard.tsx` + `RouteCopyButton.tsx`
- [ ] (2) [BEYZANUR] Zustand store'ları (wallet, goal, notification)
- [ ] (2) [BEYZANUR] TanStack Query hooks (useGoal, useGoalsList, useRouteSearch)

## Faz 3: Integration Checkpoint-1 (Saat 20-24)

- [ ] (3) [ŞEYMA+BEYZANUR] Frontend ↔ Backend SSE bağlantı testi
- [ ] (3) [ŞEYMA+NAHIDE] Backend ↔ Agents gerçek API testi (Amadeus + OpenAI)
- [ ] (3) [NAHIDE+BEYZANUR] Frontend ↔ Smart Contract (Phantom tx)
- [ ] (3) [ŞEYMA+NAHIDE] Backend ↔ Smart Contract event listener sync
- [ ] (3) [ÜÇÜ] End-to-end happy path: create → sponsor → release ✅

## Faz 4: Feature Completion (Saat 24-36)

### Backend
- [ ] (4) [ŞEYMA] Error handling + retry policy detaylandırma
- [ ] (4) [ŞEYMA] Prompt fine-tuning — 10 test goal üzerinde halüsinasyon kontrolü
- [ ] (4) [ŞEYMA] `price_history` doldurma logic'i (goal create + Celery)
- [ ] (4) [ŞEYMA] Celery worker — Fırsat Avcısı periyodik (30sn demo, 1h prod)
- [ ] (4) [ŞEYMA] WebSocket push: fiyat düşüşü → frontend modal
- [ ] (4) [ŞEYMA] Final report markdown polish (emoji, tablo, başlıklar)

### Database & DevOps
- [ ] (4) [NAHIDE] Seed data script: 20-30 fake route + embedding
- [ ] (4) [NAHIDE] Redis cache warming script (demo rotaları)
- [ ] (4) [NAHIDE] Multiple sponsor PDA testi (5 wallet, aynı goal)
- [ ] (4) [NAHIDE] Demo wallet'ları hazırlama (5 adet, faucet'tan SOL)
- [ ] (4) [NAHIDE] Solana Explorer link helper (frontend'e gömülecek)

### Frontend
- [ ] (4) [BEYZANUR] **`PriceChart.tsx`** — Recharts ile fiyat tarihçesi
- [ ] (4) [BEYZANUR] Buy signal badge + annotation
- [ ] (4) [BEYZANUR] **`DealNotificationModal.tsx`** — Human-in-the-loop
- [ ] (4) [BEYZANUR] `/profile/[wallet]` page
- [ ] (4) [BEYZANUR] Route copy akışı end-to-end
- [ ] (4) [BEYZANUR] Loading/error/empty states (tüm sayfalarda)
- [ ] (4) [BEYZANUR] Toast bildirimleri (sonner)

## Faz 5: Integration Checkpoint-2 (Saat 36-40)

- [ ] (5) [ÜÇÜ] Full demo akışı baştan sona × 2 deneme
- [ ] (5) [ÜÇÜ] Edge case testleri (Phantom red, Amadeus timeout, SSE kopması)
- [ ] (5) [NAHIDE] Demo wallet bakiyelerini kontrol & faucet refresh
- [ ] (5) [ÜÇÜ] Bug fixing buffer

## Faz 6: Polish & Demo Prep (Saat 40-48)

- [ ] (6) [BEYZANUR] UI polish — tüm ekranların görsel review'u
- [ ] (6) [BEYZANUR] Dicebear avatar entegrasyonu (wallet'tan deterministic)
- [ ] (6) [BEYZANUR] Cover image'lar (Unsplash, 4-5 görsel)
- [ ] (6) [ÜÇÜ] Demo video çekimi (3-5 dk, yedek)
- [ ] (6) [ŞEYMA] `docs/architecture.md` finalize (mimari diyagramları)
- [ ] (6) [BEYZANUR] `docs/demo-script.md` finalize (5 dk senaryo)
- [ ] (6) [ŞEYMA] Sunum slaytları — jüri kriterleri eşlemesi
- [ ] (6) [ÜÇÜ] Demo provası × 2
- [ ] (6) [ÜÇÜ] Pre-demo checklist uygula
- [ ] (6) [NAHIDE] Backup laptop hazır, mobile hotspot test
- [ ] (6) [NAHIDE] Backend production mode (`uvicorn --workers 2`)
- [ ] (6) [BEYZANUR] Frontend prod build (`next build`)
- [ ] (6) [ÜÇÜ] Phantom auto-approve KAPALI doğrula

## Cut List (Saat 30+ Panik Senaryosu)

> Sırasıyla atılabilir (en az önemliden en kritiğe):

- [ ] (CUT) Mobile responsive
- [ ] (CUT) Sosyal Rota Ağı semantic search → keyword filter'a düş
- [ ] (CUT) Route copy fonksiyonel akış (UI kalsın)
- [ ] (CUT) Refund flow UI
- [ ] (CUT) `/profile/[wallet]` page
- [ ] (CUT) Fiyat grafiği gerçek data → statik SVG fallback
- [ ] (CUT) WebSocket → polling fallback

## ASLA ATILMAYACAKLAR

- AgentStreamPanel + SSE
- Smart Contract init + sponsor + release
- Final report (Agentic AI çıktısı)
- Phantom integration
