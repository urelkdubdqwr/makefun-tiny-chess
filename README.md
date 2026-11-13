# Tiny Chess v3 — make.fun tiny-chess-01 entry

A chess engine in readable Python 3 (standard library only), built for
the make.fun tiny-chess-01 size-capped trial harness. 120-square
mailbox board, negamax search with alpha-beta pruning and quiescence,
MVV-LVA ordering plus killer moves, material + piece-square
evaluation, iterative deepening over a fixed 48,000-node budget —
fully deterministic: no clock, no randomness, same position always
yields the same move. Verified against its predecessor over a 20-game
match (14-6) and a 13-case perft suite (start position 20/400/8,902;
Kiwipete 48/2,039/97,862); slowest move observed 1.81 s against the
10 s limit.

The program runs once per trial as `python3 -P -s /bot/main.py` and
plays its games over the harness HTTP/JSON protocol (POST /game,
/move, /resign).

Entrant: @urelkdubdqwr · License: MIT
