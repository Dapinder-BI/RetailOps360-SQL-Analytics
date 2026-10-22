# RetailOps 360 — Business Questions & SQL Answers

All 15 business questions and their original query cells, collected from the [original notebooks](notebooks/original_exports/). Query text, including any `%sql` cell directive, is preserved exactly. Open the notebooks to view saved results.

<sub>🔴 Built in Databricks. In the queries, `retailops360` is the catalog and `source` is the schema.</sub>

**Quick navigation**

| No. | Analysis |
|:---:|---|
| 01 | [Top Customers by Revenue](#question-01) |
| 02 | [Customer Activation Gap](#question-02) |
| 03 | [Customer Retention & Purchase Inactivity](#question-03) |
| 04 | [Multiple Payment Transaction Analysis](#question-04) |
| 05 | [Order-to-Payment Reconciliation](#question-05) |
| 06 | [Revenue Inflation from JOIN Multiplication](#question-06) |
| 07 | [Completed Orders Without Shipments](#question-07) |
| 08 | [Late Delivery Performance](#question-08) |
| 09 | [Fully Paid Orders Without Confirmed Delivery](#question-09) |
| 10 | [Product Category Revenue Analysis](#question-10) |
| 11 | [Products Without Sales Analysis](#question-11) |
| 12 | [Product Return Rate Analysis](#question-12) |
| 13 | [Customer-Order Referential Integrity Analysis](#question-13) |
| 14 | [Orphan Payment Transaction Analysis](#question-14) |
| 15 | [Complete Order-to-Payment Integrity Reconciliation](#question-15) |

<a id="question-01"></a>

### 01. Top Customers by Revenue

**Question:** Which 10 customers generated the highest total completed-order revenue, and how many completed orders did each place?

**SQL answer** · [Source notebook](notebooks/original_exports/01_Customer_Sales_Performance_Analysis.ipynb)

```sql
%sql
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.order_amount), 2) AS total_revenue
FROM retailops360.source.customers AS c
INNER JOIN retailops360.source.orders AS o
    ON c.customer_id = o.customer_id
WHERE o.order_status = 'Completed'
GROUP BY
    c.customer_id,
    c.customer_name
ORDER BY total_revenue DESC
LIMIT 10;
```

<a id="question-02"></a>

### 02. Customer Activation Gap

**Question:** Which registered customers have never placed an order, and how long have they been registered?

**SQL answer** · [Source notebook](notebooks/original_exports/01_Customer_Sales_Performance_Analysis.ipynb)

```sql
%sql
SELECT
    c.customer_id,
    c.customer_name,
    c.signup_date,
    DATEDIFF(CURRENT_DATE(), c.signup_date)
        AS days_since_registration
FROM retailops360.source.customers AS c
LEFT ANTI JOIN retailops360.source.orders AS o
    ON c.customer_id = o.customer_id
ORDER BY days_since_registration DESC;
```

<a id="question-03"></a>

### 03. Customer Retention & Purchase Inactivity

**Question:** Which customers made completed purchases in 2025 but have not made any completed purchases in 2026?

**SQL answer** · [Source notebook](notebooks/original_exports/01_Customer_Sales_Performance_Analysis.ipynb)

```sql
%sql

WITH customers_2025 AS (
    SELECT
        c.customer_id,
        c.customer_name
    FROM retailops360.source.customers AS c
    LEFT SEMI JOIN retailops360.source.orders AS o
        ON c.customer_id = o.customer_id
       AND o.order_date >= DATE '2025-01-01'
       AND o.order_date < DATE '2026-01-01'
       AND o.order_status = 'Completed'
)
SELECT
    c.customer_id,
    c.customer_name
FROM customers_2025 AS c
LEFT ANTI JOIN retailops360.source.orders AS o
    ON c.customer_id = o.customer_id
   AND o.order_date >= DATE '2026-01-01'
   AND o.order_date < DATE '2027-01-01'
   AND o.order_status = 'Completed'
ORDER BY c.customer_id;
```

<a id="question-04"></a>

### 04. Multiple Payment Transaction Analysis

**Question:** Which orders have multiple payment transactions, and what is the combined payment amount for each order?

**SQL answer** · [Source notebook](notebooks/original_exports/02_Revenue_Payment_Reconciliation_Analysis.ipynb)

```sql
%sql
SELECT
    o.order_id,
    o.order_date,
    o.order_amount,
    COUNT(p.payment_id) AS payment_count,
    ROUND(SUM(p.payment_amount), 2) AS total_payment_amount
FROM retailops360.source.orders AS o
INNER JOIN retailops360.source.payments AS p
    ON o.order_id = p.order_id
GROUP BY
    o.order_id,
    o.order_date,
    o.order_amount
HAVING COUNT(p.payment_id) > 1
ORDER BY payment_count DESC, o.order_id;
```

<a id="question-05"></a>

### 05. Order-to-Payment Reconciliation

**Question:** Which orders are unpaid, underpaid, fully paid, or overpaid when total captured payments are compared with the order amount?

**SQL answer** · [Source notebook](notebooks/original_exports/02_Revenue_Payment_Reconciliation_Analysis.ipynb)

```sql
%sql
WITH payment_summary AS (
SELECT
        order_id,
        COUNT(payment_id) AS payment_count,
        SUM(payment_amount) AS total_paid
FROM retailops360.source.payments
    WHERE payment_status = 'Captured'
    GROUP BY order_id
),

order_reconciliation AS (
    SELECT
        o.order_id,
        o.order_date,
        o.order_amount,
        COALESCE(p.payment_count, 0) AS payment_count,
        COALESCE(p.total_paid, 0) AS total_paid
    FROM retailops360.source.orders AS o
    LEFT JOIN payment_summary AS p
        ON o.order_id = p.order_id
)

SELECT
    order_id,
    order_date,
    order_amount,
    payment_count,
    ROUND(total_paid, 2) AS total_paid,
    ROUND(order_amount - total_paid, 2) AS balance_difference,
    CASE
        WHEN total_paid = 0 THEN 'Unpaid'
        WHEN total_paid < order_amount THEN 'Underpaid'
        WHEN total_paid = order_amount THEN 'Fully Paid'
        ELSE 'Overpaid'
    END AS reconciliation_status
FROM order_reconciliation
ORDER BY order_id;
```

<a id="question-06"></a>

### 06. Revenue Inflation from JOIN Multiplication

**Question:** How much is total order revenue overstated when orders are joined directly to multiple payment transactions without preserving order-level grain?

**SQL answer** · [Source notebook](notebooks/original_exports/02_Revenue_Payment_Reconciliation_Analysis.ipynb)

```sql
%sql
WITH correct_revenue AS (
    SELECT
        SUM(order_amount) AS actual_revenue
    FROM retailops360.source.orders
    WHERE order_status = 'Completed'
),

incorrect_revenue AS (
    SELECT
        SUM(o.order_amount) AS inflated_revenue
    FROM retailops360.source.orders AS o
    INNER JOIN retailops360.source.payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'Completed'
)

SELECT
    ROUND(c.actual_revenue, 2) AS actual_revenue,
    ROUND(i.inflated_revenue, 2) AS incorrectly_joined_revenue,
    ROUND(
        i.inflated_revenue - c.actual_revenue, 2
    ) AS net_reporting_error,
    ROUND(
        (i.inflated_revenue - c.actual_revenue)
        / NULLIF(c.actual_revenue, 0) * 100,
        2
    ) AS net_error_percentage
FROM correct_revenue AS c
CROSS JOIN incorrect_revenue AS i;
```

<a id="question-07"></a>

### 07. Completed Orders Without Shipments

**Question:** Which completed orders have no shipment record, indicating a potential fulfillment backlog?

**SQL answer** · [Source notebook](notebooks/original_exports/03_Fulfillment_Delivery_Performance_Analysis.ipynb)

```sql
%sql
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.expected_delivery_date,
    o.order_amount
FROM retailops360.source.orders AS o
LEFT ANTI JOIN retailops360.source.shipments AS s
    ON o.order_id = s.order_id
WHERE o.order_status = 'Completed'
ORDER BY o.order_date, o.order_id;
```

<a id="question-08"></a>

### 08. Late Delivery Performance

**Question:** Which delivered orders arrived after their expected delivery date, and how many days late were they?

**SQL answer** · [Source notebook](notebooks/original_exports/03_Fulfillment_Delivery_Performance_Analysis.ipynb)

```sql
%sql
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.expected_delivery_date,
    s.delivered_date,
    s.shipping_method,
    DATEDIFF(
        s.delivered_date,
        o.expected_delivery_date
    ) AS days_late
FROM retailops360.source.orders AS o
INNER JOIN retailops360.source.shipments AS s
    ON o.order_id = s.order_id
WHERE s.shipment_status = 'Delivered'
    AND s.delivered_date > o.expected_delivery_date
ORDER BY days_late DESC, o.order_id;
```

<a id="question-09"></a>

### 09. Fully Paid Orders Without Confirmed Delivery

**Question:** Which fully paid, completed orders have no shipment marked as delivered, including orders with other shipment statuses?

**SQL answer** · [Source notebook](notebooks/original_exports/03_Fulfillment_Delivery_Performance_Analysis.ipynb)

```sql
WITH captured_payments AS (
    SELECT
        order_id,
        ROUND(SUM(payment_amount), 2)
            AS total_paid
    FROM retailops360.source.payments
    WHERE payment_status = 'Captured'
    GROUP BY order_id
),

fully_paid_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_date,
        o.order_amount,
        p.total_paid
    FROM retailops360.source.orders AS o
    INNER JOIN captured_payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'Completed'
      AND ABS(o.order_amount - p.total_paid) < 0.01
),

undelivered_orders AS (
    SELECT
        f.*
    FROM fully_paid_orders AS f
    LEFT ANTI JOIN retailops360.source.shipments AS s
        ON f.order_id = s.order_id
       AND s.shipment_status = 'Delivered'
)

SELECT
    u.order_id,
    u.customer_id,
    u.order_date,
    u.order_amount,
    u.total_paid,
    COALESCE(
        s.shipment_status,
        'No Shipment Record'
    ) AS shipping_status
FROM undelivered_orders AS u
LEFT JOIN retailops360.source.shipments AS s
    ON u.order_id = s.order_id
ORDER BY u.order_date, u.order_id;
```

<a id="question-10"></a>

### 10. Product Category Revenue Analysis

**Question:** Which product categories generated the highest merchandise revenue from completed orders, and how many units were sold in each category?

**SQL answer** · [Source notebook](notebooks/original_exports/04_Product_Returns_Performance_Analysis.ipynb)

```sql
SELECT
    p.category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2)
        AS total_revenue
FROM retailops360.source.orders AS o
INNER JOIN retailops360.source.order_items AS oi
    ON o.order_id = oi.order_id
INNER JOIN retailops360.source.products AS p
    ON oi.product_id = p.product_id
WHERE o.order_status = 'Completed'
GROUP BY p.category
ORDER BY total_revenue DESC;
```

<a id="question-11"></a>

### 11. Products Without Sales Analysis

**Question:** Which products have never appeared in any customer order, potentially indicating low demand or inactive inventory?

**SQL answer** · [Source notebook](notebooks/original_exports/04_Product_Returns_Performance_Analysis.ipynb)

```sql
SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.list_price
FROM retailops360.source.products AS p
LEFT ANTI JOIN retailops360.source.order_items AS oi
    ON p.product_id = oi.product_id
ORDER BY p.category, p.product_name;
```

<a id="question-12"></a>

### 12. Product Return Rate Analysis

**Question:** Which products have the highest return rates relative to the units sold, and how do those rates vary by product category?

**SQL answer** · [Source notebook](notebooks/original_exports/04_Product_Returns_Performance_Analysis.ipynb)

```sql
WITH product_sales AS (
    SELECT
        oi.product_id,
        COUNT(DISTINCT oi.order_id) AS orders_with_product
    FROM retailops360.source.order_items AS oi
    INNER JOIN retailops360.source.orders AS o
        ON oi.order_id = o.order_id
    WHERE o.order_status = 'Completed'
    GROUP BY oi.product_id
),

product_returns AS (
    SELECT
        r.product_id,
        COUNT(DISTINCT r.order_id) AS returned_orders
    FROM retailops360.source.returns AS r
    INNER JOIN retailops360.source.orders AS o
        ON r.order_id = o.order_id
    WHERE r.return_status = 'Approved'
      AND o.order_status = 'Completed'
    GROUP BY r.product_id
)

SELECT
    p.product_id,
    p.product_name,
    p.category,
    s.orders_with_product,
    COALESCE(r.returned_orders, 0) AS returned_orders,
    ROUND(
        COALESCE(r.returned_orders, 0) * 100.0
        / NULLIF(s.orders_with_product, 0),
        2
    ) AS return_rate_pct

FROM retailops360.source.products AS p

INNER JOIN product_sales AS s
    ON p.product_id = s.product_id

LEFT JOIN product_returns AS r
    ON p.product_id = r.product_id

ORDER BY
    return_rate_pct DESC,
    s.orders_with_product DESC;
```

*Interpretation:* This query measures approved-return orders as a percentage of completed orders containing each product. It does not measure returned units.

<a id="question-13"></a>

### 13. Customer-Order Referential Integrity Analysis

**Question:** Which orders reference customers who do not exist in the customer master table, including orders with missing customer IDs?

**SQL answer** · [Source notebook](notebooks/original_exports/05_Data_Quality_Order_Integrity_Analysis.ipynb)

```sql
SELECT
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.order_amount,
    CASE
        WHEN o.customer_id IS NULL
            THEN 'Missing Customer ID'
        ELSE 'Customer Not Found'
    END AS issue_type
FROM retailops360.source.orders AS o
LEFT ANTI JOIN retailops360.source.customers AS c
    ON o.customer_id = c.customer_id
ORDER BY o.order_date, o.order_id;
```

<a id="question-14"></a>

### 14. Orphan Payment Transaction Analysis

**Question:** Which payment transactions cannot be matched to a valid order, and what is their total monetary value?

**SQL answer** · [Source notebook](notebooks/original_exports/05_Data_Quality_Order_Integrity_Analysis.ipynb)

```sql
WITH orphan_payments AS (
    SELECT
        p.payment_id,
        p.order_id,
        p.payment_amount,
        p.payment_status,
        CASE
            WHEN p.order_id IS NULL
                THEN 'Missing Order ID'
            ELSE 'Order Not Found'
        END AS issue_type
    FROM retailops360.source.payments AS p
    LEFT JOIN retailops360.source.orders AS o
        ON p.order_id = o.order_id
    WHERE o.order_id IS NULL
)

SELECT
    payment_id,
    order_id,
    payment_amount,
    payment_status,
    issue_type,
    COUNT(*) OVER () AS total_orphan_payments,
    ROUND(
        SUM(payment_amount) OVER (),
        2
    ) AS total_orphan_payment_amount
FROM orphan_payments
ORDER BY payment_amount DESC, payment_id;
```

<a id="question-15"></a>

### 15. Complete Order-to-Payment Integrity Reconciliation

**Question:** Which orders and payment records fail to reconcile across both systems, including unmatched records and amount discrepancies?

**SQL answer** · [Source notebook](notebooks/original_exports/05_Data_Quality_Order_Integrity_Analysis.ipynb)

```sql
WITH payment_summary AS (
    SELECT
        order_id,
        ROUND(
            SUM(
                CASE
                    WHEN payment_status = 'Captured'
                        THEN payment_amount
                    ELSE 0
                END
            ),
            2
        ) AS captured_amount,
        COUNT(payment_id) AS payment_count
    FROM retailops360.source.payments
    GROUP BY order_id
),

reconciliation AS (
    SELECT
        o.order_id AS order_id,
        p.order_id AS payment_order_id,
        o.order_amount,
        p.captured_amount,
        p.payment_count
    FROM retailops360.source.orders AS o
    FULL OUTER JOIN payment_summary AS p
        ON o.order_id = p.order_id
)

SELECT
    COALESCE(order_id, payment_order_id)
        AS reference_order_id,

    order_amount,

    COALESCE(captured_amount, 0)
        AS captured_amount,

    COALESCE(payment_count, 0)
        AS payment_count,

    ROUND(
        COALESCE(order_amount, 0)
        - COALESCE(captured_amount, 0),
        2
    ) AS amount_difference,

    CASE
        WHEN order_id IS NULL
            THEN 'Orphan Payment'

        WHEN payment_order_id IS NULL
            THEN 'No Payment Record'

        WHEN captured_amount = 0
            THEN 'No Captured Payment'

        WHEN captured_amount < order_amount
            THEN 'Underpaid'

        WHEN captured_amount > order_amount
            THEN 'Overpaid'

        ELSE 'Fully Reconciled'
    END AS reconciliation_status

FROM reconciliation

WHERE order_id IS NULL
   OR payment_order_id IS NULL
   OR captured_amount <> order_amount

ORDER BY reconciliation_status, reference_order_id;
```

