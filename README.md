# RetailOps 360 — E-Commerce Operations & Revenue Analytics

**A Databricks SQL portfolio project that investigates customer activity, payment discrepancies, fulfillment exceptions, product performance, and data integrity across a fictional Canadian e-commerce business.**

## Business problem

Retail teams need to understand what happens between a customer placing an order, the business collecting payment, and the customer receiving the products. Those events are recorded in separate tables, often with multiple payment transactions, order lines, or shipment records for a single order.

Without a reconciled view of that lifecycle, teams can miss customers who never buy or stop purchasing, overlook payment discrepancies and delivery exceptions, and misinterpret product demand or returns. Reporting can also overstate revenue when one-to-many joins duplicate order amounts.

**RetailOps 360 addresses this visibility gap by using SQL to connect operational records, identify exceptions, and produce evidence that Sales, Finance, Operations, Merchandising, and Data teams can investigate and act on.**

This is a synthetic case study. The issues above frame the investigation; they are not claims about a real company's performance.

## Business questions and decisions

| Business area | Questions investigated | Decision supported |
|---|---|---|
| Customer & Sales | Who are the top customers by completed-order value? Who has never ordered? Which 2025 buyers have no completed purchases in 2026? | Prioritize customer relationship, activation, and re-engagement efforts. |
| Revenue & Payments | Which orders have multiple payments? Which are unpaid, underpaid, fully paid, or overpaid? How can joins inflate reported order value? | Prioritize reconciliation exceptions and improve the reliability of financial reporting. |
| Fulfillment & Delivery | Which completed orders have no shipment? Which deliveries arrived late? Which fully paid orders have no confirmed delivery? | Identify orders for fulfillment review and customer follow-up. |
| Products & Returns | Which categories drive merchandise value and units sold? Which products have no orders? Which products have high return rates? | Guide assortment reviews and investigate return patterns. |
| Data Quality & Integrity | Which orders lack valid customers? Which payments lack valid orders? Which records or amounts fail reconciliation? | Prioritize data corrections and strengthen reporting controls. |

These analyses identify patterns and exceptions for review. A missing shipment record does not by itself prove an order was never shipped, and purchase inactivity does not by itself establish customer churn.

## Project scope and status

- **Platform:** Databricks SQL and Unity Catalog
- **Source:** `retailops360.source`
- **Dataset:** Synthetic Canadian e-commerce data across 8 related tables; approximately 311,025 rows in the prepared dataset
- **Period represented:** January 2024–September 2026
- **Published work:** 15 business questions across 5 notebooks, with saved result previews and original executed HTML reports
- **SQL focus:** JOINs, relationships, filtering, grouping, NULL handling, and table grain
- **Planned:** Databricks AI/BI dashboard and a consolidated findings summary

The notebook copies were reconstructed from executed Databricks HTML exports. Saved tabular previews contain up to 100 rows per query; preview row counts should not be treated as full result counts. Data generation and loading scripts are not currently included in this repository.

## Explore the analyses

GitHub renders the notebooks with business questions, SQL, and saved result previews.

| Questions | GitHub notebook | Original Databricks export |
|---|---|---|
| 01–03 | [Customer & Sales Performance](notebooks/01_Customer_Sales_Performance_Analysis.ipynb) | [HTML report](notebook_reports/01_Customer_Sales_Performance_Analysis.html) |
| 04–06 | [Revenue & Payment Reconciliation](notebooks/02_Revenue_Payment_Reconciliation_Analysis.ipynb) | [HTML report](notebook_reports/02_Revenue_Payment_Reconciliation_Analysis.html) |
| 07–09 | [Fulfillment & Delivery Performance](notebooks/03_Fulfillment_Delivery_Performance_Analysis.ipynb) | [HTML report](notebook_reports/03_Fulfillment_Delivery_Performance_Analysis.html) |
| 10–12 | [Product & Returns Performance](notebooks/04_Product_Returns_Performance_Analysis.ipynb) | [HTML report](notebook_reports/04_Product_Returns_Performance_Analysis.html) |
| 13–15 | [Data Quality & Order Integrity](notebooks/05_Data_Quality_Order_Integrity_Analysis.ipynb) | [HTML report](notebook_reports/05_Data_Quality_Order_Integrity_Analysis.html) |

GitHub's source view does not render the HTML reports. Open the notebook links to read queries and results directly on GitHub.

## Data model and measurement approach

The dataset contains `customers`, `customer_addresses`, `products`, `orders`, `order_items`, `payments`, `shipments`, and `returns`. See the [source data model](data_model/DATA_MODEL.md) for intended table grain and conceptual relationships.

Reliable analysis depends on keeping the measures distinct:

- **Completed-order value:** Order amounts for orders meeting the analysis's completed-status criteria.
- **Merchandise value:** Order-line value used to analyze products and categories.
- **Captured payments:** Eligible payment transactions used to reconcile money collected against order amounts.
- **Delivery confirmation:** Shipment records marked as delivered, evaluated separately from order and payment status.

Aggregate one-to-many records at the required grain before joining. Multiple payments or shipments can be valid operational events; investigate them in context. Validate status values, NULL handling, return linkage, and date filters before interpreting results.

## Repository structure

```text
RetailOps360-SQL-Analytics/
├── README.md
├── index.html
├── data_model/
│   └── DATA_MODEL.md
├── notebooks/
│   ├── 01_Customer_Sales_Performance_Analysis.ipynb
│   ├── 02_Revenue_Payment_Reconciliation_Analysis.ipynb
│   ├── 03_Fulfillment_Delivery_Performance_Analysis.ipynb
│   ├── 04_Product_Returns_Performance_Analysis.ipynb
│   └── 05_Data_Quality_Order_Integrity_Analysis.ipynb
├── notebook_reports/
│   ├── index.html
│   └── [5 executed Databricks HTML reports]
└── dashboard/
    └── screenshots/  [placeholder for planned dashboard]
```

## Next steps

1. Consolidate validated findings, exception counts, and business recommendations from the five published analyses.
2. Document reproducible dataset setup and KPI definitions.
3. Build a Databricks AI/BI dashboard and add screenshots.

_All data is synthetic and does not represent transactions or customers of a real company. No business improvement or financial impact is claimed without supporting evidence._
