# Architecture Overview

## System Components

```
Frontend (Next.js)  ←→  Backend (FastAPI)  ←→  PostgreSQL + pgvector
                              ↕                        ↕
                         AI Agents               Redis (cache + queue)
                         (LangGraph)                   ↕
                              ↕                   Celery Worker
                    External APIs:
                    - OpenAI GPT-4o
                    - Amadeus (flights/hotels)
                    - Google Maps

Frontend ←→ Solana Devnet ←→ travel_escrow Program (Anchor)
```

## Data Flow

1. User creates a goal via `/create` form
2. Backend saves goal to DB, starts SSE stream
3. Orchestrator spawns Route + Deal agents in parallel (`asyncio.gather`)
4. Budget agent runs after both complete
5. Final report compiled and saved to DB
6. SSE stream emits `done` event → frontend redirects to goal detail

## SSE Events

| Event | Payload |
|---|---|
| `agent_start` | `{ agent, goal_id }` |
| `agent_complete` | `{ agent, data }` |
| `done` | `{ goal_id, report }` |
| `error` | `{ message }` |

## Smart Contract (Anchor)

- **TravelGoal PDA**: `[b"goal", goal_id.as_bytes()]`
- **Sponsorship PDA**: `[b"sponsorship", goal_pubkey, sponsor_pubkey]`
- Authority = backend keypair → controls `release_funds` and `refund_sponsor`
