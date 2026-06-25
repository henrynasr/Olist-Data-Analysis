# Olist E-Commerce Analysis

End-to-end business analytics project on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (99,441 orders, 2016–2018) plus a separate [B2B marketing funnel dataset](https://www.kaggle.com/datasets/olistbr/marketing-funnel-olist) (8,000 leads → 842 closed deals).

**→ [Full analysis notebook](./olist_analysis.ipynb)**

## What's covered
- **Marketing & Sales Funnel (B2B):** lead-to-close conversion, by origin and segment, sales cycle length, seller acquisition tracking gap
- **Customer Behavior (B2C):** retention, AOV, delivery wait vs satisfaction, cancelled orders, retention by category
- **Sellers & Products:** best-selling categories, best-performing sellers
- **Operational Performance:** delivery estimate accuracy, seller dispatch lateness, freight cost ratio by state

## Stack
PostgreSQL · DBeaver · Python (pandas, SQLAlchemy, matplotlib) · Jupyter · Power BI

## Notes
- Data cleaning policy, null/typo audits, and a mid-project bug fix (duplicate-timestamp inflating "returning customer" counts) are documented inline in the notebook.
- Power BI dashboard: see `/powerbi` folder.
