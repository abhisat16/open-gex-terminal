# Open GEX Terminal

GexBot-Classic-style dealer gamma exposure (GEX) levels, computed entirely in your browser from Cboe's free, 15-minute-delayed option chains.

**Live site:** https://abhisat16.github.io/open-gex-terminal/

## What it shows
- GEX by strike (open interest and volume), call walls / put walls (Major ±), zero gamma (spline crossing between the majors, GexBot's documented method) and the GEX-vs-price profile flip
- Classic view: intraday price, zero-gamma and major-level lines with GEX bars on the same price axis, max-change GEX, history playback (build it by loading several snapshots)
- Volatility smile with call/put volume, 3D dealer-gamma and implied-volatility surfaces
- Futures conversion: additive basis for SPX→ES / NDX→NQ, price ratio for ETFs (GLD→GC, SPY→ES, QQQ→NQ); one-click Gold mode
- Light and dark themes

## How to use
1. On cboe.com open an underlying's options page (e.g. SPX, NDX, GLD), set Options Range: All and Expiration: All, and click **Download CSV**.
2. Drop the file onto the page. Nothing is uploaded; all maths runs locally.
3. Optional: type the live futures price (ES / NQ / GC) in Settings to convert levels.

## Method
Per contract: GEX = Γ × OI (or volume) × 100 × S² × 0.01, calls positive and puts negative (naive dealer convention). Γ is recomputed with Black–Scholes from Cboe's implied volatility.

Research and education only. Not financial advice. Data © Cboe; this repository contains no Cboe data.
