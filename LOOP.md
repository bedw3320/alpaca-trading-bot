# Loop Constitution

This repository is the entire trading runtime. Do not import, submodule, or share secrets with any other personal project. Secrets stay in `.env` (gitignored) on the machine that runs IB Gateway.

This file is **harness law**, not strategy. Strategy YAML comes later.

## Planes

| Plane | Where | Allowed to |
|---|---|---|
| Brain | Cursor (Mini local, or Cloud **read-only**) | Research, propose `OrderIntent`, write journals |
| Hands | This process + IB Gateway on the Mini | Connect to IBKR, place / cancel / flatten |
| Broker | IBKR **paper** (default) or live (armed) | Fills |
| Memory | `state/state.db` + git | Events, strategies, this constitution |

Cursor Cloud must not hold TWS passwords and must not place orders. IBKR’s public MCP (`https://api.ibkr.com/v1/api/mcp-public`) is analysis only — it is not an execution API. Confirm-in-TWS is a valid Phase-0 path; unattended live is not.

## Four constraints (inviolable)

1. **LLM proposes. Code places.** An `OrderIntent` (`schemas/output.py`) is not an order. Execution requires preview → single-use confirmation token → place, with risk **re-validated at send**. Today this is **not implemented**: `core/agent.py::create_order` and `core/runner.py` still send in one hop. Closing that gap is the next code change.

2. **Hands fail closed on identity.** Before any place, code must verify the connected IBKR account id and paper/live flag match config. A `TRADING_MODE=paper` label sitting on a live Gateway port is a hard abort. Today this is **not implemented**: `integrations/ibkr/client.py` connects to host/port and trusts the env label.

3. **Autonomy is armed, not implied.** Default: propose and journal, do not send. `--allow-trading` enables paper sends only when `TRADING_MODE=paper`. Live requires `TRADING_MODE=live` **and** `--allow-trading` **and** an explicit autonomy arm that can latch off on daily loss or Gateway disconnect. Human-confirmed explicit tickets are not silently resized.

4. **Process skills ≠ broker.** Cursor / Claude skills (pre-trade check, execution-plan check, debrief) never call `ib_insync`. Broker I/O lives in `integrations/ibkr/` (later: a local MCP wrapping the same). Scheduled cycles default to dry-run (journal only).

## Current gates that stay

- `TRADING_MODE` defaults to `paper` (Gateway paper port **4002**)
- `--allow-trading` / `ALLOW_TRADING` default false
- Runner enforces `max_daily_trades`, `max_position_pct`, `max_total_exposure_pct` in **code** (`core/runner.py`)
- Confidence threshold (default 0.75) skips the trade
- Append-only SQLite event log (`utils/state.py`)
- `docker-compose.yml`: `ib-gateway` + `agent`, Gateway healthcheck before the agent starts

## Cycle (target)

`dry` → research → `OrderIntent` → code risk → preview token → (human **or** armed autonomy) → place → fill log → stop.

Until constraints 1–2 ship in code, do not arm live. Paper with `--allow-trading` is still one-hop; treat it as a Gateway connectivity test, not as the target loop.

## Isolation

No shared env files, Cursor environment wiring, or knowledge imports from any other personal repo. Trading knowledge lives in `knowledge/` here.
