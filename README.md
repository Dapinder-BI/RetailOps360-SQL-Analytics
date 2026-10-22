# RetailOps 360 — E-Commerce Operations & Revenue Analytics

**A Databricks SQL analytics engineering portfolio project** investigating the customer-to-order-to-payment-to-delivery lifecycle of a fictional Canadian e-commerce business.

## Project overview

RetailOps 360 uses a synthetic, relational e-commerce dataset to explore practical questions from Sales, Finance, Operations, Merchandising, and Data Quality teams. The focus is **SQL Phase 1: JOINs, relationships, filtering, grouping, NULL handling, and table grain**. Analysis is developed and validated in Databricks before exported notebooks and result reports are published here.

- **Technology:** Databricks SQL, Unity Catalog, Databricks AI/BI Dashboards (planned)
- **Source location:** `retailops360.source`
- **Synthetic data:** 8 related tables; approximately 311,025 rows in the prepared dataset
- **Timeline represented:** January 2024–September 2026
- **Scope:** 15 business questions across 5 analysis notebooks

> **Status:** Executed HTML reports for Notebooks 01–03 are published. Source notebook exports, remaining analyses, and dashboard are planned. No query outputs are fabricated.

## Business investigations

| Notebook | Questions | Business analysis | Focus |
|---|---|---|---|
| 01 | 01–03 | Customer & Sales Performance | High-value customers; never-purchased customers; inactive buyers |
| 02 | 04–06 | Revenue & Payment Reconciliation | Multiple payments; payment gaps; revenue errors from JOIN multiplication |
| 03 | 07–09 | Fulfillment & Delivery Performance | Unshipped orders; late deliveries; paid-but-undelivered orders |
| 04 | 10–12 | Product & Returns Performance | Category demand; products without sales; returns |
| 05 | 13–15 | Data Quality & Order Integrity | Orphaned records; unmatched payments; reconciliation exceptions |

## Repository structure

```text
RetailOps360-SQL-Analytics/
├── README.md
├── data_model/
│   └── DATA_MODEL.md
├── notebooks/
│   ├── 01_Customer_Sales_Performance_Analysis.ipynb  [published]
│   └── 02_Revenue_Payment_Reconciliation_Analysis.ipynb  [published]
├── notebook_reports/
│   ├── 01_Customer_Sales_Performance_Analysis.html  [published]
│   └── 02_Revenue_Payment_Reconciliation_Analysis.html  [published]
└── dashboard/
    └── screenshots/  [planned]
```

## View notebooks directly on GitHub

GitHub renders the following Jupyter notebook files with Markdown explanations, SQL code, and saved result previews:

- [Notebook 01 — Customer & Sales Performance (view code and results)](notebooks/01_Customer_Sales_Performance_Analysis.ipynb)
- [Notebook 02 — Revenue & Payment Reconciliation (view code and results)](notebooks/02_Revenue_Payment_Reconciliation_Analysis.ipynb)
- [Notebook 03 — Fulfillment & Delivery Performance (view code and results)](notebooks/03_Fulfillment_Delivery_Performance_Analysis.ipynb)

These GitHub-viewable copies were reconstructed from the original Databricks HTML exports. Table previews are capped at 100 rows for readability; original exports remain in `notebook_reports/`. The notebook cells contain `%sql` commands as used in Databricks.

## Executed Databricks HTML notebooks

- [Notebook 01 — Customer & Sales Performance Analysis](notebook_reports/01_Customer_Sales_Performance_Analysis.html) — Questions 01–03, SQL and exported query results.
- [Notebook 02 — Revenue & Payment Reconciliation Analysis](notebook_reports/02_Revenue_Payment_Reconciliation_Analysis.html) — Questions 04–06, SQL and exported query results.
- [Notebook 03 — Fulfillment & Delivery Performance Analysis](notebook_reports/03_Fulfillment_Delivery_Performance_Analysis.html) — Questions 07–09, SQL and exported query results.

**View notebooks as rendered webpages:** Enable GitHub Pages in repository Settings → Pages, selecting *Deploy from a branch*, *main*, and */ (root)*. After the site is published, open `https://dapinder-bi.github.io/RetailOps360-SQL-Analytics/notebook_reports/` to browse the original HTML exports with their saved SQL and results. Ordinary GitHub `blob` links show HTML source rather than rendering it. HTML reports are supplementary to editable notebook source files still to be added.

## Data model

Eight tables: `customers`, `customer_addresses`, `products`, `orders`, `order_items`, `payments`, `shipments`, and `returns`. See [data model](data_model/DATA_MODEL.md) for their purposes and relationships.

## Analytical principles

- Preserve the **grain** of each table when joining across one-to-many relationships.
- Distinguish **orders**, **merchandise value**, and **captured payments** instead of treating them as interchangeable revenue measures.
- Use the actual dataset's payment and order status values when calculating KPIs.
- Investigate and explain exceptions, not merely produce SQL output.
- Publish executed notebook exports, results, and business interpretations after validation.

## Roadmap

1. Validate source data and relationships in Databricks.
2. Complete and export Notebooks 01–03.
3. Complete the remaining three analysis notebooks.
4. Validate KPI calculations, NULL handling, and JOIN cardinalities.
5. Develop a Databricks AI/BI dashboard.
6. Add findings, visual evidence, and final project documentation.

_All data is synthetic and does not represent transactions or customers of a real company._
