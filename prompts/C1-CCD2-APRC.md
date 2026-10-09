# Task: APRC computations under the EU Consumer Credit Directive assumptions

Compute the Annual Percentage Rate of Charge for the four credit scenarios below, step by step. The APRC is the rate X solving the standard present-value equation (sum of drawdowns discounted at X equals sum of repayments and charges discounted at X, periods in years, actuarial method). Your iteration/bisection steps must be shown — at least the first three iterations and the convergence check — because the solver will be re-run mechanically against your intermediate values.

1. **Simple fixed loan:** €10,000 drawn at t=0; 24 equal monthly repayments of €450 starting one month after drawdown; a €100 arrangement fee paid at t=0. Compute APRC to 1 decimal place.
2. **Overdraft assumption case:** credit limit €3,000; per the directive's additional assumptions, assume the full amount is drawn for the whole duration; duration assumed 3 months where not determinable; borrowing rate 12% nominal per annum charged monthly; a €25 monthly account fee. State each assumption you invoked, then compute.
3. **Open-end credit assumption case:** limit €1,500 drawn immediately in full; repayment assumed in 12 equal monthly instalments (state the assumption's source-logic); rate 18% nominal per annum monthly compounding; no other fees. Compute.
4. **Unascertainable-drawdown case:** limit €5,000; assume drawdown of the full amount at t=0 (state why); repayment as a single payment at 12 months; rate 8% nominal; €200 broker fee financed into the balance at t=0. Compute, and state how the financed fee enters the equation differently than a t=0 cash fee.

**Output:** bare JSON only: `[{"case": N, "assumptions_invoked": ["..."], "equation": "<the PV equation with your numbers>", "iterations": "<first 3 + convergence>", "aprc_pct": X.X}]` plus `{"weakest_point": "..."}` — the assumption or computational step most likely to diverge from the directive's exact method.
