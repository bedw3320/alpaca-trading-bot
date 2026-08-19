# Options Trading Bot

Standalone Interactive Brokers trading runtime. Not part of any other personal repo.

## Read first

1. `LOOP.md` — harness law (planes, four constraints, current vs target)
2. `CLAUDE.md` — file map, commands, how to run
3. `.claude/rules/02-trading-safety.md` — live-trading gates

Do not answer execution questions from memory. The loop constitution wins over any skill, command, or prior chat.

## Isolation

Do not import, submodule, copy secrets from, or write into any other personal project. `.env` and IB Gateway stay on the machine that trades.

## Defaults

- Paper. Trading disabled until `--allow-trading`.
- LLM proposes `OrderIntent`. Code places orders. One-hop `create_order` is a known gap (`LOOP.md` constraint 1) — do not add more one-hop paths.
- No strategy work in a harness session unless asked.
