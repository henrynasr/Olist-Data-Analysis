# Diagnosing R$15.7M in Olist E-Commerce Revenue: Retention, Delivery, and B2B Funnel Analysis

End-to-end SQL + Python analysis of a real Brazilian e-commerce platform (99,441 orders, 2016–2018) plus its B2B sales funnel (8,000 leads → 842 closed deals). Caught and fixed two data-integrity bugs that were silently corrupting prior conclusions before delivering 8 directed recommendations.

**→ [Full notebook](./olist_analysis.ipynb)**

## Executive Summary

**Business problem:** Olist has scale — R$15.7M in revenue, 3,095 sellers, an active B2B sales funnel — but no quantified answer to where it's losing money. Retention, delivery reliability, seller quality, and catalog allocation had never been measured against each other.

**Solution:** Built the full pipeline from raw CSVs (11 relational tables, 1M+ geolocation rows) into PostgreSQL, queried with SQL, analyzed in Python. Ran retention/cohort analysis, delivery accuracy checks, funnel conversion analysis, and seller performance ranking — with a z-test layer to separate real anomalies from noise in small-sample states and categories.

**Impact, in numbers:**
- **96.6% of customers buy once.** Returners spend the same as first-timers (R$149 vs R$148) — retention is a *volume* problem, not a value problem. Upsell tactics won't fix it.
- **Delivery estimates are wrong by design**: every state and category delivers earlier than promised — worst cases 18–20 days early (AC, RO, AP, AM). Olist is sacrificing checkout conversion to protect an already-bulletproof on-time rate.
- **construction_tools_house_garden = 8% of B2B deals but 82% of B2B revenue** — and it's the *slowest* segment to close (61 days vs 30 for phone_mobile).
- **One seller (7c67e144) dispatches late on 30.6% of items** — 4–5x worse than its top-5 peers — and posts the weakest review score (3.3) of the group. Two independent metrics, same root cause.
- **40 of 71 product categories sit below a R$100K revenue floor**, despite 1–2 years live — settled dead weight, not a ramp-up issue.
- Found and corrected a **duplicate-timestamp bug** that inflated the returning-customer count by 257 false positives (2,997 → corrected **2,740**).

**Next steps:** Power BI dashboard (in progress) to make these 8 findings stakeholder-ready without opening the notebook.

## Recommendations

Ordered by leverage.

1. **Fix lead-source and seller-acquisition tracking.** 88% of sellers have no acquisition record; the best-"converting" origin is untracked `unknown`. Every funnel conclusion here covers 12% of the seller base. Closing this gap is what makes future funnel analysis trustworthy.

2. **Concentrate B2B effort on `construction_tools_house_garden`, but cut its closing friction.** 82% of closed-deal revenue, yet the slowest segment to close (61 days), concentrated in slow origins. Confirm margin before reallocating budget — this is revenue, not profit.

3. **Treat retention as a volume problem, not a spend problem.** Only ~3% of customers return, and they spend the same as first-timers — upsell tactics won't move this. Seed new customers into `bed_bath_table` / `furniture_decor` / `sports_leisure`, which over-index among returners (correlational, test it). Delivery speed has no measurable effect on return — not a lever here.

4. **Treat AC, RO, AP, AM as one structural problem: distance from the SP logistics core.** Highest freight ratio (23–26% vs SP's 14%), most over-padded delivery estimates (~3 weeks early), high AOV but low volume. Recalibrate delivery estimates here first — zero risk to on-time rate, since actuals already beat the promise by 15–20 days. Test subsidized freight before ad spend.

5. **Split high-AOV states by delivery readiness before marketing.** AP, PB, AC, RO already score 4.1–4.2 satisfaction — advertise now. AL is the exception: worst score (3.8) on a 24.5-day wait — fix delivery first.

6. **Flag RO for a fulfillment review.** Cancel/unavailable rate 2.77%, ~2.2x national, statistically confirmed (z=2.19, p=0.014). Root cause not investigated here — hand to ops.

7. **Cut catalog dead weight; replicate the Mar–Jun 2018 fulfillment window.** 40 of 71 categories sit below R$100K after 1–2 years live — reallocate catalog/promo spend to proven performers. Separately, Mar–Jun 2018 was the lowest-cancellation stretch on record — identify the driver and reproduce it.

8. **Investigate seller `7c67e144`.** #2 by revenue, but flagged by two independent metrics: weakest review score (3.3) and 30.6% late-dispatch rate (4–5x peers). Lateness is a credible cause of the low score — worth a direct intervention.

## Method — and why

| Step | Choice | Why |
|---|---|---|
| Storage | PostgreSQL, not flat-file pandas | 11 relational tables with real FK structure — tests actual join/schema reasoning, not just CSV wrangling |
| Query drafting | DBeaver scratchpad → notebook | Mirrors a real workflow: validate logic in a SQL client before it goes into a reproducible pipeline |
| Cleaning | Pandas only, never on raw Postgres tables | Raw data stays reproducible from source CSVs at all times — no `UPDATE`/`DELETE` on the source of truth |
| Revenue metric | `SUM(price + freight_value)` from `order_items`, not `SUM(payment_value)` | `payment_value` double-counts split/voucher payment rows (one order had 29 voucher rows) — confirmed via fan-out check; switching the metric changed a state-level category ranking (PR) |
| Returning-customer flag | `COUNT(DISTINCT order_purchase_timestamp)`, not `order_id` | Found 290 customers with duplicate `order_id` rows sharing the same timestamp — inflated retention count by 257 false positives (2,997 → corrected 2,740) |
| Significance testing | z-test vs. national baseline | Separates real anomalies (RO cancellations, z=2.19, p=0.014) from noise in small-sample states/categories |
| Revenue scope | Exclude `canceled`/`unavailable` orders from all revenue queries | Quantified the inflation first (R$108K, ~0.68% of total) — small, but kept as standard practice going forward |

## Skills demonstrated

**SQL:** CTEs, window functions (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`), joins (`LEFT JOIN` to preserve unreviewed orders vs. `INNER JOIN`), `CASE WHEN`, aggregates (`SUM`, `COUNT(DISTINCT ...)`), subqueries, FK-aware schema design (11 tables, PKs + FKs)

**Python:** pandas (cleaning, groupby, merge-fan-out diagnosis), matplotlib/seaborn (distribution, survival-curve, and cohort visualization), SQLAlchemy (Postgres ↔ Jupyter), psycopg2

**Analysis:** cohort/retention analysis, z-test significance testing, funnel conversion analysis, two-layer data-quality auditing (null audit + typo/value-level audit), bug root-causing in production-style queries

## What more time or better data would unlock

- **No clickstream/web data** (page views, sessions, bounce, device) — bounce rate by source, cart abandonment, and checkout drop-off can't be answered on this dataset. Scoped into a separate planned project (REES46 clickstream data).
- **No profit/margin data** — revenue-based recommendations (e.g., fast-tracking `construction_tools_house_garden`) can't be weighed against margin. Flagged as a gap, not assumed away.
- **Seller acquisition tracking covers only 12.3% of sellers** (380/3,095 trace to a `closed_deals` record) — can't attribute seller performance back to acquisition channel for the other 88%.
- **Cut by scope, not by difficulty**: per-state seller ranking and a full purchase→approved→carrier→delivered stage-by-stage latency breakdown were both designed (including the outlier z-test method) but parked — country-level findings and the existing delivery analysis were judged sufficient for this round.
- **Month-of-year seasonality** on cancellation rate — not assessable with under two years of data.

## Stack

PostgreSQL · DBeaver · Python (pandas, SQLAlchemy, matplotlib) · Jupyter · Power BI

## Repo notes

- Full null-audit, typo-audit, and the duplicate-timestamp bug fix (root cause + before/after numbers) are documented inline in the notebook, not just summarized here.
- Power BI dashboard: `/powerbi` (exported page images included so it's viewable without opening Power BI Desktop).