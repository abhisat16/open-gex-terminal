# Open GEX Terminal

A free, GexBot-style options positioning terminal (Classic + State views), computed entirely in your browser from Cboe's free, ~15-minute-delayed option chains.

**Live site:** https://abhisat16.github.io/open-gex-terminal/ (the previous version stays at `/v1.html`)

## Views
- **classic**: naive GEX ladder by volume (bright bars) and open interest (faint bars) on the same price axis as the spot candles. Major positive / negative levels for volume (left labels) and open interest (right labels), zero gamma (cubic-spline crossing between the majors, GexBot's documented method), net GEX, max-change GEX over 1/5/10/15/30 minutes, lookback dots, history playback. Scopes: 90d (agg), latest (0DTE), next (1DTE).
- **state**: options profile (taker long/short calls and puts), DEX, convexity (gamma), −vanna ex and charm ex ladders, and the GEX profile (net call vs put imbalance), with 0DTE IV skew dots and the ±1σ expected move.
- **levels**: call wall, put wall, zero gamma and net GEX for every loaded ticker, in futures terms.

## Data
- Daily snapshot files (`SYM_YYYY-MM-DD_gex.csv`, `#GEXSNAP` format) with the matching futures price inside; select several at once.
- Cboe CSV exports or Cboe JSON.
- **Live link**: a bookmark button run on a cboe.com page sends a snapshot every minute (SPX, NDX, GLD). Snapshots are kept in the browser (IndexedDB) for the session.

## Method
- GEX = Γ × contracts × 100 × S² × 1%, calls positive and puts negative. Γ, Δ, vanna and charm are recomputed with Black–Scholes from Cboe's implied volatility.
- **State uses a proxy for trade classification.** GexBot classifies each trade from tick data. Here each snapshot's new volume is split taker-long / taker-short by where the contract's last trade sits inside its bid/ask, accumulated through the session.
- DEX = net × Δ × 100 × S · convexity = net × Γ × 100 × S² × 1% · −vanna ex = net × vanna × (−IV) × 100 × S · charm ex = net × charm × 100 × S / 8760 per hour.
- Expected move = S × ATM IV (50/25/25 three-strike smoothing) × √(time to 4 pm ET in days / 365).
- Futures: additive basis for SPX→ES and NDX→NQ, price ratio for GLD→GC.

Research and education only. Not financial advice. Data © Cboe; this repository contains no Cboe data.
