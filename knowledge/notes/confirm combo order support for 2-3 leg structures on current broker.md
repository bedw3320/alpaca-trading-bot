---
description: "Open: verify IBKR combo (BAG) orders for 2-3 leg risk reversals including a protection put"
category: open-question
created: 2026-02-20
updated: 2026-08-19
source: "research_v0_ Options Risk Reversal Strategy.md"
confidence: experimental
topics: ["[[open-questions]]"]
---

Unresolved: confirm `ib_insync` combo / BAG orders for 2-3 leg options structures on Interactive Brokers. Risk reversals need the short put and long call filled together; defined-risk versions add a third leg (protection put). If combo orders are not wired in `integrations/ibkr/orders.py` yet, legging in sequentially means slippage risk.

IBKR TWS supports combo contracts. This repo's order path is still single-leg (`MarketOrder` / `LimitOrder` on one contract). That is the gap — not a broker choice.

## Connections
- [[the zero-cost calibration algorithm starts at 20-delta put and finds the call strike matching the credit]]
- [[defined-risk structures are recommended for EM positions buying 10-delta put protection]]

---
*Topics: [[open-questions]]*
