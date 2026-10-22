# RetailOps 360 — Data model

Eight related tables support the customer, payment, fulfillment, product, and data integrity analyses in the [project overview](../README.md). The data is synthetic, and monetary values are in CAD.

## Tables and keys

Each row represents the business record described below. Keys describe the logical relationships in the dataset; the setup script does not declare database key constraints.

| Table | One row represents | Identifier | Related keys |
|---|---|---|---|
| `customers` | A registered customer | `customer_id` | — |
| `customer_addresses` | A customer's saved billing or shipping address | `address_id` | `customer_id` → customers |
| `orders` | A customer order | `order_id` | `customer_id` → customers |
| `order_items` | A product line within an order | `order_item_id` | `order_id` → orders; `product_id` → products |
| `products` | A catalog product | `product_id` | — |
| `payments` | A payment transaction | `payment_id` | `order_id` → orders |
| `shipments` | An order's shipment record | `shipment_id` | `order_id` → orders |
| `returns` | A return request for a product on an order | `return_id` | `order_id` → orders; `product_id` → products |

## Relationships

The [README diagram](../README.md#data-model-overview) provides the visual overview. These relationships describe the supplied dataset.

| Parent → related table | Relationship |
|---|---|
| Customers → Customer addresses | Each customer has one billing and one shipping address. |
| Customers → Orders | A customer can have no orders or multiple orders. Each order belongs to one customer. |
| Orders → Order items | Each order contains one or more product lines. |
| Products → Order items | A product can appear on no order lines or multiple order lines. |
| Orders → Payments | An order can have no payments or multiple payment transactions. |
| Orders → Shipments | An order has no shipment record or one shipment record. |
| Orders → Returns | An order has no return request or one return request. |
| Products → Returns | A product can appear in no return requests or multiple return requests. |

A return references both an order and a product on that order. It does not link directly to `order_item_id`.

## Measurement rules

- **Completed-order value:** Sum `orders.order_amount` for orders marked `Completed`, counting each order once. The amount equals the sum of quantity × unit price across its order lines and excludes tax and shipping fees.
- **Merchandise value:** Use `order_items.quantity × order_items.unit_price` for product and category analysis. Apply the same completed-order filter when comparing with completed-order value.
- **Captured payments:** Sum `payments.payment_amount` where `payment_status = 'Captured'`. Aggregate by order before comparing with `orders.order_amount`; payment totals and order value are separate measures.
- **Delivery confirmation:** Use `shipments.shipment_status = 'Delivered'`. Compare `delivered_date` with `orders.expected_delivery_date` to identify late deliveries. Order completion and payment do not establish delivery.
- **Returns:** Each record is a request, with status `Approved`, `Requested`, or `Rejected`. The product return-rate query divides completed orders with an approved return for a product by completed orders containing that product. The table has no returned quantity or refund amount, so this is an order-based rate, not a unit-based or refund rate.

## Joining and interpreting the data

Aggregate order items and payments separately to order level before combining their totals. Joining both detail tables directly can multiply records and overstate amounts. Filter addresses to Billing or Shipping when one address per customer is needed.

Missing payments or shipment records are intentional business scenarios. Foreign keys in the supplied dataset are valid, so orphan-record checks may return no exceptions. A missing shipment record indicates a review item; it does not prove the order was never shipped.

See the [dataset guide](../data/README.md) for loading instructions and the [setup script](../scripts/setup_databricks.sql) for column definitions.
