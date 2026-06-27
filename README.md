# Olist Revenue Diagnostics: Why 96.6% of Customers Never Come Back

End-to-end SQL + Python analysis of a real Brazilian e-commerce platform (99,441 orders, 2016–2018) plus its B2B sales funnel (8,000 leads → 842 closed deals). Built to answer one question: **where is Olist leaving money on the table, and what should it fix first?**

**→ [Full notebook](./olist_analysis.ipynb)**

## Executive Summary

**Problem:** Olist has scale (R$15.7M in revenue, 3,095 sellers) but no clarity on where it's bleeding value — retention, delivery, seller quality, and catalog spend were never quantified.

**Solution:** Built the analytics pipeline from raw CSVs (11 tables, 1M+ geolocation rows) → PostgreSQL → SQL → Python, ran retention/cohort, delivery, funnel, and seller-performance analysis, caught and fixed 2 data-integrity bugs that were silently corrupting prior conclusions, delivered 8 recommendations.

**Impact, in numbers:**
- **96.6% one-time buyer rate** — retention is a volume problem, not a value problem (returning customers spend the same: R$149 vs R$148)
- **Delivery estimates are wrong by design**: every state/category delivers early — worst offenders 18-20 days early (AC, RO, AP, AM) — Olist is sacrificing checkout conversion to protect an already-bulletproof on-time rate
- **construction_tools_house_garden = 8% of deals but 82% of B2B revenue** — yet closes slowest (61 days) of any major segment
- **1 seller (7c67e144) dispatches late on 30.6% of items**, 3x worse than its next-closest peer, and posts the weakest review score (3.3) of the top 5 — two independent metrics, same root cause
- **40 of 71 product categories sit below a R$100K revenue floor**, despite 1-2 years of live sales — not a ramp-up issue, a dead-weight catalog issue

**Next steps:** Power BI dashboard (in progress) to make these 8 findings interview/stakeholder-ready without opening the notebook.

## Method — and why

| Step | Choice | Why |
|---|---|---|
| Storage | PostgreSQL, not flat-file pandas | 11 relational tables with real FK structure — tests actual join/schema reasoning, not just CSV wrangling |
| Query drafting | DBeaver scratchpad → notebook | Mirrors real workflow: validate logic in SQL client before it goes in a reproducible pipeline |
| Cleaning | Pandas only, never on raw Postgres tables | Raw data stays reproducible from source CSVs at all times — no `UPDATE`/`DELETE` on the source of truth |
| Revenue metric | `SUM(price + freight_value)` from `order_items`, not `SUM(payment_value)` | `payment_value` double-counts split/voucher payment rows — confirmed via fan-out check, switching metric changed a state-level category ranking (PR) |
| Returning-customer flag | `COUNT(DISTINCT order_purchase_timestamp)`, not `order_id` | Found 290 customers with duplicate `order_id` rows sharing the same timestamp — inflated retention count by 257 false positives (2,997 → corrected 2,740) |
| Significance testing | z-test vs national baseline (e.g. cancellation rate by state/category) | Distinguishes real anomalies (RO cancellations, p=0.014) from noise in small-sample states/categories |

## Skills demonstrated

**SQL:** CTEs, window functions (`ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`), joins (`LEFT JOIN` to preserve unreviewed orders vs `INNER JOIN`), `CASE WHEN`, aggregates (`SUM`, `COUNT(DISTINCT ...)`), subqueries, FK-aware schema design

**Python:** pandas (cleaning, groupby, merge-fan-out diagnosis), matplotlib/seaborn (distribution, survival-curve, and cohort visualization), SQLAlchemy (Postgres↔Jupyter), psycopg2

**Analysis:** cohort/retention analysis, z-test significance testing, funnel conversion analysis, data-quality auditing (null + typo/value-level), bug root-causing in production-style queries

## What more time / better data would unlock

- **No clickstream/web data** (page views, sessions, bounce, device) — bounce rate by source, cart abandonment, and checkout drop-off can't be answered on this dataset; scoped into a separate planned project (REES46 clickstream data)
- **No profit/margin data** — revenue-based recommendations (e.g. fast-tracking `construction_tools_house_garden`) can't be weighed against margin; flagged as a gap, not assumed away
- **Seller acquisition tracking only covers 12.3% of sellers** (380/3,095 trace to a `closed_deals` record) — can't attribute seller performance back to acquisition channel for the other 88%
- **Cut by scope, not by difficulty**: per-state seller ranking and a full purchase→approved→carrier→delivered stage-by-stage latency breakdown were both designed (outlier z-test method included) but parked — country-level findings and existing delivery analysis were judged sufficient for this round

## Stack

PostgreSQL · DBeaver · Python (pandas, SQLAlchemy, matplotlib) · Jupyter · Power BI

## Repo notes

- Full null-audit, typo-audit, and the duplicate-timestamp bug fix (with root cause and before/after numbers) are documented inline in the notebook, not just summarized here
- Power BI dashboard: `/powerbi` (exported page images included so it's viewable without opening Power BI / Desktop)
