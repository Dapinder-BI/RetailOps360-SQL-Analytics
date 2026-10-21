# RetailOps 360 — E-Commerce Operations & Revenue Analytics

**A Databricks SQL analytics engineering portfolio project** investigating the customer-to-order-to-payment-to-delivery lifecycle of a fictional Canadian e-commerce business.

## Project overview

RetailOps 360 uses a synthetic, relational e-commerce dataset to explore practical questions from Sales, Finance, Operations, Merchandising, and Data Quality teams. The focus is **SQL Phase 1: JOINs, relationships, filtering, grouping, NULL handling, and table grain**. Analysis is developed and validated in Databricks before exported notebooks and result reports are published here.

- **Technology:** Databricks SQL, Unity Catalog, Databricks AI/BI Dashboards (planned)
- **Source location:** `retailops360.source`
- **Synthetic data:** 8 related tables; approximately 311,025 rows in the prepared dataset
- **Timeline represented:** January 2024–September 2026
- **Scope:** 15 business questions across 5 analysis notebooks

> **Status:** Repository setup in progress. The executed Databricks notebook exports and business insights will be uploaded after verification. No query outputs are fabricated.

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
│   ├── 01_Customer_Sales_Performance_Analysis.ipynb  [to upload]
│   └── 02_Revenue_Payment_Reconciliation_Analysis.ipynb  [to upload]
├── reports/
│   ├── 01_Customer_Sales_Performance_Analysis.html  [to upload]
│   └── 02_Revenue_Payment_Reconciliation_Analysis.html  [to upload]
└── dashboard/
    └── screenshots/  [planned]
```

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
2. Complete and export Notebooks 01 and 02.
3. Complete the remaining three analysis notebooks.
4. Validate KPI calculations, NULL handling, and JOIN cardinalities.
5. Develop a Databricks AI/BI dashboard.
6. Add findings, visual evidence, and final project documentation.

_All data is synthetic and does not represent transactions or customers of a real company._
