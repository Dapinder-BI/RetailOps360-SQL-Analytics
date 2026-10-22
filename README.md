# RetailOps 360 — E-Commerce Operations & Revenue Analytics

![RetailOps 360 project banner](data_model/assets/project-banner-v2.svg)

[![Business problem](https://img.shields.io/badge/Business%20problem-123750?style=for-the-badge)](#business-problem) [![Business value](https://img.shields.io/badge/Business%20value-123750?style=for-the-badge)](#business-value) [![Data model](https://img.shields.io/badge/Data%20model-123750?style=for-the-badge)](#data-model-overview) [![15 questions](https://img.shields.io/badge/15%20questions-123750?style=for-the-badge)](#business-questions) [![Dataset](https://img.shields.io/badge/Dataset-123750?style=for-the-badge)](#dataset) [![Notebooks](https://img.shields.io/badge/Notebooks-123750?style=for-the-badge)](#explore-the-analyses) [![Skills](https://img.shields.io/badge/Skills-123750?style=for-the-badge)](#skills-developed)

[![SQL answers](https://img.shields.io/badge/SQL%20answers-0D9488?style=for-the-badge)](BUSINESS_QUESTIONS_AND_SQL.md)

**An e-commerce business analysis project covering customers, payments, deliveries, products, and returns.**

<sub>🔴 Built in Databricks. In the queries, `retailops360` is the catalog and `source` is the schema.</sub>

<a id="business-problem"></a>

## 🎯 Business problem

Retail teams lack a clear view of unpaid orders, delayed deliveries, inactive customers, and product returns. This makes it difficult to protect revenue, resolve service issues, and prioritize action.

RetailOps 360 brings these issues together to help teams identify what needs attention and make informed decisions.

<a id="business-value"></a>

## 💡 Business value

- **Protect revenue:** Identify unpaid orders and payment discrepancies for follow-up.
- **Improve customer experience:** Highlight delivery issues and opportunities to re-engage customers.
- **Support product decisions:** Understand demand and return patterns.
- **Build confidence in reporting:** Reconcile records and prevent double-counting.

![From business questions to decisions](data_model/assets/project-workflow.svg)

<a id="business-areas-and-decisions"></a>

## 🧭 Business areas and decisions

| Business area | Decision supported |
|---|---|
| Customer & Sales | Prioritize customer activation, retention, and re-engagement. |
| Revenue & Payments | Resolve payment discrepancies and improve revenue reporting. |
| Fulfillment & Delivery | Prioritize delayed or unshipped orders and customer follow-up. |
| Products & Returns | Review product demand, assortment, and high return rates. |
| Data Quality & Integrity | Correct unmatched records and improve reporting accuracy. |

These analyses identify patterns and exceptions for review. A missing shipment record does not by itself prove an order was never shipped, and purchase inactivity does not by itself establish customer churn.

<a id="data-model-overview"></a>

## 🗂️ Data model overview

Eight connected tables follow the customer journey from purchase to payment, delivery, and returns.

```mermaid
flowchart LR
    C["CUSTOMERS<br/>One record per customer"]
    A["CUSTOMER ADDRESSES<br/>One record per saved address"]
    O["ORDERS<br/>One record per order"]
    I["ORDER ITEMS<br/>One record per order line"]
    P["PRODUCTS<br/>One record per product"]
    PAY["PAYMENTS<br/>One record per transaction"]
    S["SHIPMENTS<br/>One record per shipment"]
    R["RETURNS<br/>One record per return"]

    C -->|"1 → 2 address types"| A
    C -->|"1 → many"| O
    O -->|"1 → many"| I
    P -->|"1 → many"| I
    O -->|"1 → many"| PAY
    O -->|"1 → 0 or 1"| S
    O -->|"1 → 0 or 1"| R
    P -->|"1 → many"| R

    classDef customer fill:#EFF6FF,stroke:#2563EB,color:#172554,stroke-width:1.5px;
    classDef order fill:#0F172A,stroke:#0F172A,color:#FFFFFF,stroke-width:2px;
    classDef product fill:#F0FDFA,stroke:#0D9488,color:#134E4A,stroke-width:1.5px;
    classDef operation fill:#F8FAFC,stroke:#64748B,color:#1E293B,stroke-width:1.5px;
    class C,A customer;
    class O order;
    class I,P product;
    class PAY,S,R operation;
```

**Reading the model:** Each customer has a billing and a shipping address and can have no orders or multiple orders. Each order can have multiple items and payments, with at most one shipment and one return in this dataset. Each return also references a product. See the [data model documentation](data_model/DATA_MODEL.md) for keys and relationships.

<a id="business-questions"></a>

**15 business questions**

| No. | Business question |
|:---:|---|
| 1 | Which 10 customers have the highest completed-order value, and how many completed orders did each place? |
| 2 | Which registered customers have never ordered, and how long have they been registered? |
| 3 | Which customers purchased in 2025 but have no completed purchases in 2026? |
| 4 | Which orders have multiple payment transactions, and what is the total payment amount for each? |
| 5 | Which orders are unpaid, underpaid, fully paid, or overpaid compared with captured payments? |
| 6 | How much can order value be overstated when multiple payment records cause orders to be counted more than once? |
| 7 | Which completed orders have no shipment record? |
| 8 | Which deliveries arrived after the expected date, and how many days late were they? |
| 9 | Which fully paid, completed orders have no confirmed delivery? |
| 10 | Which product categories have the highest merchandise value and units sold from completed orders? |
| 11 | Which products have never appeared in a customer order? |
| 12 | Which products have the highest approved-return rates by completed order, and which categories do they belong to? |
| 13 | Which orders have missing customer IDs or reference customers absent from the customer records? |
| 14 | Which payments cannot be matched to an order, and what is their total value? |
| 15 | Which orders and payments fail reconciliation because of unmatched records or amount differences? |

<a id="dataset"></a>

## 📁 Dataset

[Browse the eight CSV files](data/) · [Data model](data_model/DATA_MODEL.md)

The dataset covers customers, orders, products, payments, deliveries, and returns. All customer names and transactions are fictional; monetary values are in CAD.

- [Dataset guide](data/README.md)
- [Reproducible data generator](scripts/generate.py)
- [Table setup and loading script](scripts/setup_databricks.sql)

The source data has valid foreign keys. Missing payments, shipments, and other related records are intentional scenarios; integrity checks can return no orphan records.

<a id="project-scope"></a>

## 📌 Project scope

- **Source:** `retailops360.source`
- **Dataset:** Synthetic Canadian e-commerce data across 8 related tables
- **Order dates:** January 2024–September 2026
- **Published work:** 15 business questions across 5 notebooks, with saved result previews and original notebook exports

Saved outputs are previews and may not contain the full query results. The dataset, generator, and loading script are linked in the Dataset section.

<a id="explore-the-analyses"></a>

## 📖 Explore the analyses

![Explore the analyses: questions, queries, and saved results](data_model/assets/analyses-banner.svg)

**Quick access:** [All 15 business questions and SQL answers](BUSINESS_QUESTIONS_AND_SQL.md)

Open the GitHub notebooks below to read business questions, queries, and saved result previews. The [original notebook exports](notebooks/original_exports/) also preserve the supplied queries and saved outputs for download.

| Questions | GitHub notebook |
|---|---|
| 01–03 | [Customer & Sales Performance](notebooks/01_Customer_Sales_Performance_Analysis.ipynb) |
| 04–06 | [Revenue & Payment Reconciliation](notebooks/02_Revenue_Payment_Reconciliation_Analysis.ipynb) |
| 07–09 | [Fulfillment & Delivery Performance](notebooks/03_Fulfillment_Delivery_Performance_Analysis.ipynb) |
| 10–12 | [Product & Returns Performance](notebooks/04_Product_Returns_Performance_Analysis.ipynb) |
| 13–15 | [Data Quality & Order Integrity](notebooks/05_Data_Quality_Order_Integrity_Analysis.ipynb) |

Open the notebook links to read queries and saved results directly on GitHub.

<a id="measurement-approach"></a>

## 📐 Measurement approach

Completed-order value, merchandise value, captured payments, and confirmed deliveries are measured separately. Return records represent requests rather than refunded amounts or confirmed quantities returned.

See the [data model documentation](data_model/DATA_MODEL.md) for table definitions, relationships, and measurement rules.

<a id="skills-developed"></a>

## 🛠️ Skills developed

| Skill | Applied in this project |
|---|---|
| Business analysis | Translated business problems into 15 focused analytical questions. |
| Data relationships and joins | Connected related tables using inner, outer, semi, and anti joins. |
| Aggregation and CTEs | Built grouped summaries and structured multi-step queries. |
| Payment reconciliation | Compared captured payments with order amounts to identify discrepancies. |
| Accurate measurement | Preserved table grain and prevented double-counting across joins. |
| Data quality checks | Checked missing relationships, unmatched records, and order integrity. |
| Customer and operational analysis | Examined purchase inactivity, delivery delays, product demand, and returns. |
| Databricks and documentation | Worked with catalogs, schemas, and notebooks; published queries and results on GitHub. |

<a id="repository-structure"></a>

## 📂 Repository structure

```text
RetailOps360/
├── README.md
├── BUSINESS_QUESTIONS_AND_SQL.md
├── index.html
├── data/  [8 CSV files and dataset guide]
├── scripts/  [generator and loading script]
├── data_model/
│   └── DATA_MODEL.md
└── notebooks/
    ├── 01_Customer_Sales_Performance_Analysis.ipynb
    ├── 02_Revenue_Payment_Reconciliation_Analysis.ipynb
    ├── 03_Fulfillment_Delivery_Performance_Analysis.ipynb
    ├── 04_Product_Returns_Performance_Analysis.ipynb
    ├── 05_Data_Quality_Order_Integrity_Analysis.ipynb
    └── original_exports/  [supplied notebooks with saved outputs]
```

_All data is synthetic and does not represent transactions or customers of a real company. No business improvement or financial impact is claimed without supporting evidence._
