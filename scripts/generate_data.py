import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("data/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)


def random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)


def generate_customers(num_customers=1000):
    first_names = [
        "Ali", "Sara", "Ahmed", "Ayesha", "Bilal",
        "Fatima", "Usman", "Hira", "Hamza", "Zara"
    ]

    last_names = [
        "Khan", "Ahmed", "Malik", "Ali", "Sheikh",
        "Raza", "Hussain", "Iqbal", "Shah", "Butt"
    ]

    cities = [
        "Lahore",
        "Karachi",
        "Islamabad",
        "Rawalpindi",
        "Faisalabad"
    ]

    records = []

    start = datetime(2023, 1, 1)
    end = datetime(2026, 8, 31)

    for customer_id in range(1, num_customers + 1):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)

        records.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": f"{first_name.lower()}.{last_name.lower()}{customer_id}@example.com",
                "city": random.choice(cities),
                "signup_date": random_date(start, end).date()
            }
        )

    return pd.DataFrame(records)


def generate_products(num_products=100):
    categories = {
        "Electronics": (50, 1500),
        "Clothing": (10, 200),
        "Home": (15, 500),
        "Beauty": (5, 150),
        "Sports": (10, 400)
    }

    records = []

    for product_id in range(1, num_products + 1):
        category = random.choice(list(categories.keys()))
        min_price, max_price = categories[category]

        records.append(
            {
                "product_id": product_id,
                "product_name": f"{category} Product {product_id}",
                "category": category,
                "price": round(random.uniform(min_price, max_price), 2),
                "is_active": random.choice([True, True, True, False])
            }
        )

    return pd.DataFrame(records)


def generate_orders(customers, num_orders=5000):
    statuses = [
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    ]

    records = []

    start = datetime(2024, 1, 1)
    end = datetime(2026, 8, 31)

    customer_ids = customers["customer_id"].tolist()

    for order_id in range(1, num_orders + 1):
        records.append(
            {
                "order_id": order_id,
                "customer_id": random.choice(customer_ids),
                "order_date": random_date(start, end),
                "order_status": random.choice(statuses)
            }
        )

    return pd.DataFrame(records)


def generate_order_items(orders, products):
    records = []
    order_item_id = 1

    product_ids = products["product_id"].tolist()
    price_lookup = products.set_index("product_id")["price"].to_dict()

    for order_id in orders["order_id"]:
        number_of_items = random.randint(1, 5)

        for _ in range(number_of_items):
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 4)
            unit_price = price_lookup[product_id]

            records.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": round(quantity * unit_price, 2)
                }
            )

            order_item_id += 1

    return pd.DataFrame(records)


def generate_payments(orders, order_items):
    methods = [
        "credit_card",
        "debit_card",
        "paypal",
        "bank_transfer",
        "cash_on_delivery"
    ]

    payment_statuses = [
        "successful",
        "successful",
        "successful",
        "failed",
        "refunded"
    ]

    order_totals = (
        order_items
        .groupby("order_id")["line_total"]
        .sum()
        .to_dict()
    )

    records = []

    for _, order in orders.iterrows():
        order_id = order["order_id"]

        records.append(
            {
                "payment_id": str(uuid.uuid4()),
                "order_id": order_id,
                "payment_method": random.choice(methods),
                "payment_status": random.choice(payment_statuses),
                "amount": round(order_totals[order_id], 2),
                "payment_date": order["order_date"] + timedelta(
                    minutes=random.randint(1, 120)
                )
            }
        )

    return pd.DataFrame(records)


def main():
    print("Generating ecommerce data...")

    customers = generate_customers()
    products = generate_products()
    orders = generate_orders(customers)
    order_items = generate_order_items(orders, products)
    payments = generate_payments(orders, order_items)

    datasets = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments
    }

    for name, dataframe in datasets.items():
        output_path = OUTPUT_DIR / f"{name}.csv"

        dataframe.to_csv(
            output_path,
            index=False
        )

        print(
            f"{name}: "
            f"{len(dataframe):,} rows -> "
            f"{output_path}"
        )

    print("Data generation complete.")


if __name__ == "__main__":
    main()