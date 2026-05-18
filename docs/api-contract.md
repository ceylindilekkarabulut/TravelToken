# API Contract

## Goals

| Method | Path | Description |
|---|---|---|
| POST | `/api/goals/create` | Create goal, returns SSE stream |
| GET | `/api/goals/{id}` | Get goal by ID |
| GET | `/api/goals/list/by-wallet?user_wallet=` | List goals for wallet |
| GET | `/api/goals/{id}/price-history` | Price history for charts |

## Sponsorships

| Method | Path | Description |
|---|---|---|
| POST | `/api/sponsorships/create` | Record sponsorship after on-chain tx |
| GET | `/api/sponsorships/{goal_id}` | List sponsorships for goal |

## Routes

| Method | Path | Description |
|---|---|---|
| GET | `/api/routes/search?query=` | Hybrid search routes |
| POST | `/api/routes/{id}/copy` | Copy a route (increments counter) |

## Agents

| Method | Path | Description |
|---|---|---|
| POST | `/api/agents/approve-purchase` | Human-in-the-loop deal approval |

## WebSocket

| Path | Description |
|---|---|
| `WS /ws/notifications/{wallet}` | Real-time deal push notifications |
