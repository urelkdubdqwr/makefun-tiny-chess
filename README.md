# Tiny Chess — make.fun tiny-chess-01 entry

A chess engine in 4,031 bytes of readable Python 3 (standard library
only), written for the make.fun tiny-chess-01 size-capped trial harness.
120-square mailbox board, negamax search with alpha-beta pruning and
quiescence, MVV-LVA move ordering, material + piece-square evaluation,
iterative deepening over a fixed 12,000-node budget — fully
deterministic: no clock, no randomness, same position always yields the
same move.

The program runs once per trial as `python3 -P -s /bot/main.py` and
plays its games over the harness HTTP/JSON protocol (POST /game, /move,
/resign). Perft-verified move generation (start position 20/400/8,902;
Kiwipete 48/2,039/97,862).

Entrant: @urelkdubdqwr · License: MIT
