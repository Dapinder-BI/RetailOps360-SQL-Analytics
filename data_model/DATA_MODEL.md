# RetailOps 360 — Source Data Model

**Platform:** Databricks Unity Catalog  
**Source:** `retailops360.source`  
**Data:** Synthetic Canadian e-commerce operational records.

## Entities and intended grain

| Table | Intended grain | Main identifier | Relationship |
|---|---|---|---|
| `customers` | One customer | `customer_id` | Parent of orders and addresses |
| `customer_addresses` | One saved customer address | Address identifier | Many addresses per customer |
| `products` | One product | `product_id` | Parent of order items |
| `orders` | One order | `order_id` | Many orders per customer |
| `order_items` | One order line | Order-item identifier | Many lines per order; each line references a product |
| `payments` | One payment transaction | `payment_id` | Potentially multiple payments per order |
| `shipments` | One shipment record | Shipment identifier | May be multiple shipments per order |
| `returns` | One return record | Return identifier | References an ordered product/transaction |

## Conceptual relationships

```text
customers (1) ─── (many) orders
    │                   ├── (many) order_items ─── (many-to-one) products
    └── (many) addresses├── (many) payments
                        ├── (many) shipments
                        └── (many) returns
```

## Analytical cautions

- An order joined directly to multiple payments can multiply its order amount.
- Joining order items and payments on `order_id` can create a many-to-many combination.
- Aggregate each one-to-many relationship at the relevant grain before reconciling.
- Sum only eligible payment statuses when interpreting **money received**.
- Distinguish order status and payment status from actual settlement and delivery.
- Validate column names, counts, return linkage, and primary-key uniqueness against the deployed source tables.

The precise physical schema and key names should be confirmed from the Databricks source tables before treating this conceptual model as a tested database contract.
