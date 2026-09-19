# Finance

> Grak wider canon seed 8 of 9. The money half of the coin-logic side: pricing, risk, and the market's actual mechanics.

**Why the house keeps it.** The house trades 15-minute binaries, but the same arithmetic prices every vendor contract, every build-vs-buy, every "just add more instances" argument. Finance is the discipline of pricing the future without lying about the uncertainty.

## Canon

- **Louis Bachelier**, *Théorie de la spéculation* (1900): random walks in prices, five years before Einstein; options priced before Black-Scholes.
- **Irving Fisher**, *The Theory of Interest* (1930): present value; the rate that equates time preferences.
- **Benjamin Graham and David Dodd**, *Security Analysis* (1934): margin of safety; price is what you pay, value is what you get.
- **Harry Markowitz** (1952): portfolio selection; diversification as covariance, not count.
- **William Sharpe, John Lintner, Jan Mossin** (1964-66): CAPM; beta and the risk premium.
- **Franco Modigliani and Merton Miller** (1958): capital structure irrelevance in a frictionless world; every deviation is a friction story.
- **Fischer Black, Myron Scholes, Robert Merton** (1973): options pricing; assumptions stated, then priced.
- **Eugene Fama** (1965-70): efficient markets; the null hypothesis the house must beat to earn its rent.
- **John Kelly Jr.** (1956): bet sizing from information theory; growth rate over payout.
- **Maureen O'Hara**, *Market Microstructure Theory* (1995): order books, spreads, adverse selection.
- **Marcos López de Prado**, *Advances in Financial Machine Learning* (2018): backtest overfitting; the seven sins as a checklist.

## Working toolkit

- **Time value.** PV = FV/(1+r)^t; annuities and perpetuities; NPV (accept if > 0), IRR (the rate where NPV = 0), payback as a smell test only.
- **Valuation.** DCF from free cash flow; terminal values and why they dominate; multiples (P/E, EV/EBITDA) as comparables, not truths; dividend discount.
- **Bonds.** Price and yield move inversely; duration as first-order sensitivity, convexity as second; credit spreads; yield curve shapes (normal, inverted) as information.
- **Portfolios.** Expected return, variance, covariance, correlation; the efficient frontier; diversification reduces variance only in proportion to covariance; Sharpe ratio (excess return per unit volatility).
- **CAPM.** E[R] = R_f + β(E[R_m] − R_f); β as sensitivity to the market; alpha as the residual the model cannot explain.
- **Factors.** Value, size, momentum, quality, low volatility; a factor is a hypothesis about risk or mispricing, never a guarantee.
- **Derivatives.** Forwards and futures (cost of carry, basis); options (payoff, intrinsic vs time value); put-call parity; Black-Scholes and its assumptions (lognormal returns, no frictions, continuous hedging); the Greeks: delta, gamma, vega, theta, rho.
- **Risk.** Volatility; VaR and its blind spot (tail shape); expected shortfall; maximum drawdown; leverage arithmetic (a 50% loss needs a 100% gain to recover).
- **Bet sizing.** Expected value per bet; Kelly fraction f* = edge/odds; fractional Kelly when the estimate is uncertain (always).
- **Microstructure.** Limit order book; bid-ask spread; maker vs taker; adverse selection; market impact; slippage; latency as a cost, not an edge.
- **Rates and FX.** Compounding conventions; real vs nominal (Fisher equation); interest rate parity; purchasing power parity (loose long-run, unreliable short-run).

## Method

1. Price the claim before liking the story: cash flows, discount rate, uncertainty. If any of the three is missing, the story is not a valuation.
2. State the null: fairly priced. The burden is on the deviation, with a mechanism named.
3. Account for frictions before fees: spread, impact, funding, taxes. A strategy that dies at ten basis points was never alive.
4. Size by ruin, not by greed: survive first; Kelly or below, never above.
5. Measure both halves: entry cost and realized outcome; a win rate without net entry cost is a hymn.

## Failure modes

- Leverage ruin: LTCM at 20+; a sure convergence with a margin call is not sure.
- Survivorship and selection bias in any backtest dataset.
- Overfitting: enough knobs will fit noise; hold out, then paper first.
- Ignoring fees, spread, and slippage; the strategy that only works at zero cost.
- Unrealized PnL treated as money; marks are opinions, fills are facts.
- Correlation breakdown in crises: diversification among cousins is not diversification (August 2007).
- Selling tail risk for steady pennies (Volmageddon): the hedge that ruins its holders is not a hedge.
- VaR as a maximum loss guarantee; it is a quantile, and the tail past it is where ruin lives.
- Mistaking a rising market for skill; beta does not sign the P&L.

## Exam map

Papers: FN1 through FN5 (valuation, markets and instruments, derivatives, portfolio and risk, microstructure). Record: `GRAK_CREDENTIALS.md` lines under coin-logic.
