"""
Synthetic sales dataset generator.

Generates realistic synthetic retail sales data for the
Databricks GenAI Data Analyst Copilot portfolio project.

No real personal information is used.
"""

from pathlib import Path
import random

import numpy as np
import pandas as pd


# ============================================================
# Configuration
# ============================================================

SEED = 42
NUM_ORDERS = 10_000

START_DATE = "2025-01-01"
END_DATE = "2026-06-30"

OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "sales.csv"


# ============================================================
# Reproducibility
# ============================================================

random.seed(SEED)
np.random.seed(SEED)


# ============================================================
# Reference data
# ============================================================

REGIONS = {
    "Asia Pacific": [
        "Japan",
        "India",
        "Singapore",
        "Australia",
    ],
    "Europe": [
        "Germany",
        "France",
        "United Kingdom",
        "Italy",
    ],
    "North America": [
        "United States",
        "Canada",
    ],
    "Middle East": [
        "United Arab Emirates",
        "Saudi Arabia",
    ],
}


PRODUCTS = [
    ("P001", "Laptop Pro 14", "Electronics", 1200, 820),
    ("P002", "Laptop Air 13", "Electronics", 950, 650),
    ("P003", "Smartphone X", "Electronics", 800, 500),
    ("P004", "Smartphone Lite", "Electronics", 450, 280),
    ("P005", "Wireless Headphones", "Accessories", 180, 95),
    ("P006", "Mechanical Keyboard", "Accessories", 140, 75),
    ("P007", "Ergonomic Mouse", "Accessories", 80, 40),
    ("P008", "4K Monitor", "Electronics", 500, 310),
    ("P009", "Office Chair", "Furniture", 420, 250),
    ("P010", "Standing Desk", "Furniture", 650, 390),
    ("P011", "Desk Lamp", "Furniture", 90, 45),
    ("P012", "USB-C Dock", "Accessories", 160, 90),
    ("P013", "Tablet Pro", "Electronics", 700, 430),
    ("P014", "Tablet Mini", "Electronics", 400, 250),
    ("P015", "Webcam HD", "Accessories", 110, 55),
    ("P016", "External SSD", "Storage", 180, 105),
    ("P017", "Portable SSD", "Storage", 130, 75),
    ("P018", "Network Router", "Networking", 220, 130),
    ("P019", "WiFi Mesh System", "Networking", 350, 210),
    ("P020", "Business Projector", "Electronics", 900, 560),
]


SALES_CHANNELS = [
    "Online",
    "Retail Store",
    "Partner",
]


ORDER_STATUSES = [
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Completed",
    "Returned",
    "Cancelled",
]


FIRST_NAMES = [
    "Alex",
    "Jordan",
    "Taylor",
    "Morgan",
    "Casey",
    "Riley",
    "Avery",
    "Jamie",
    "Cameron",
    "Drew",
    "Sam",
    "Charlie",
    "Robin",
    "Elliot",
    "Harper",
    "Quinn",
]


LAST_NAMES = [
    "Smith",
    "Johnson",
    "Brown",
    "Davis",
    "Wilson",
    "Taylor",
    "Anderson",
    "Thomas",
    "Martin",
    "Jackson",
    "White",
    "Harris",
    "Clark",
    "Lewis",
    "Walker",
    "Hall",
]


# ============================================================
# Helper functions
# ============================================================

def build_customer_names(num_customers: int) -> dict:
    """Create synthetic customer names."""

    customers = {}

    for index in range(1, num_customers + 1):
        customer_id = f"C{index:05d}"

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        customers[customer_id] = f"{first_name} {last_name}"

    return customers


def choose_region_and_country():
    """Randomly select a region and country."""

    region = random.choice(list(REGIONS.keys()))
    country = random.choice(REGIONS[region])

    return region, country


def choose_product():
    """Select a product."""

    product = random.choice(PRODUCTS)

    return {
        "product_id": product[0],
        "product_name": product[1],
        "category": product[2],
        "unit_price": product[3],
        "unit_cost": product[4],
    }


def generate_discount():
    """Generate a realistic discount percentage."""

    discount_options = [
        0.00,
        0.00,
        0.00,
        0.05,
        0.05,
        0.10,
        0.10,
        0.15,
        0.20,
    ]

    return random.choice(discount_options)


def generate_quantity():
    """Generate purchase quantity."""

    return int(
        np.random.choice(
            [1, 2, 3, 4, 5, 6, 8, 10],
            p=[
                0.35,
                0.25,
                0.15,
                0.10,
                0.06,
                0.04,
                0.03,
                0.02,
            ],
        )
    )


def generate_order_status():
    """Generate order status."""

    return random.choice(ORDER_STATUSES)


# ============================================================
# Main generation
# ============================================================

def generate_sales_data():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Create customers.
    #
    # Fewer customers than orders means customers can make
    # multiple purchases, which is useful for customer analytics.
    num_customers = 1_500

    customers = build_customer_names(num_customers)

    customer_ids = list(customers.keys())

    dates = pd.date_range(
        start=START_DATE,
        end=END_DATE,
        freq="D",
    )

    rows = []

    for order_number in range(1, NUM_ORDERS + 1):

        order_id = f"O{order_number:06d}"

        order_date = random.choice(dates)

        customer_id = random.choice(customer_ids)
        customer_name = customers[customer_id]

        region, country = choose_region_and_country()

        product = choose_product()

        quantity = generate_quantity()

        unit_price = product["unit_price"]

        discount = generate_discount()

        status = generate_order_status()

        sales_channel = random.choice(SALES_CHANNELS)

        # ----------------------------------------------------
        # Calculate financial metrics
        # ----------------------------------------------------

        gross_revenue = quantity * unit_price

        revenue = gross_revenue * (1 - discount)

        cost = quantity * product["unit_cost"]

        profit = revenue - cost

        # Cancelled orders produce no realized revenue.
        if status == "Cancelled":
            revenue = 0.0
            profit = 0.0

        # Returned orders are represented as zero realized
        # revenue for simplicity.
        elif status == "Returned":
            revenue = 0.0
            profit = 0.0

        rows.append(
            {
                "order_id": order_id,
                "order_date": order_date.date(),
                "customer_id": customer_id,
                "customer_name": customer_name,
                "region": region,
                "country": country,
                "product_id": product["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "quantity": quantity,
                "unit_price": round(unit_price, 2),
                "discount": round(discount, 4),
                "revenue": round(revenue, 2),
                "cost": round(cost, 2),
                "profit": round(profit, 2),
                "sales_channel": sales_channel,
                "order_status": status,
            }
        )

    df = pd.DataFrame(rows)

    # ========================================================
    # Intentionally introduce a small number of data-quality
    # issues.
    #
    # These are useful later when we demonstrate Silver-layer
    # cleansing and automated data-quality validation.
    # ========================================================

    # Duplicate a few records.
    duplicate_rows = df.sample(
        n=10,
        random_state=SEED,
    )

    df = pd.concat(
        [df, duplicate_rows],
        ignore_index=True,
    )

    # Introduce a few missing customer names.
    missing_name_indices = df.sample(
        n=5,
        random_state=SEED + 1,
    ).index

    df.loc[
        missing_name_indices,
        "customer_name",
    ] = None

    # Introduce a few invalid quantities.
    invalid_quantity_indices = df.sample(
        n=3,
        random_state=SEED + 2,
    ).index

    df.loc[
        invalid_quantity_indices,
        "quantity",
    ] = 0

    # Introduce a few invalid discounts.
    invalid_discount_indices = df.sample(
        n=3,
        random_state=SEED + 3,
    ).index

    df.loc[
        invalid_discount_indices,
        "discount",
    ] = 1.5

    # Sort by date and order.
    df = df.sort_values(
        by=[
            "order_date",
            "order_id",
        ]
    ).reset_index(drop=True)

    # Save.
    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    return df


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    sales_df = generate_sales_data()

    print("=" * 70)
    print("Synthetic Sales Dataset Generated")
    print("=" * 70)

    print(f"Output file : {OUTPUT_FILE}")
    print(f"Rows        : {len(sales_df):,}")
    print(f"Columns     : {len(sales_df.columns)}")

    print("\nDate range:")
    print(
        sales_df["order_date"].min(),
        "to",
        sales_df["order_date"].max(),
    )

    print("\nRegions:")
    print(
        sales_df["region"]
        .value_counts()
        .to_string()
    )

    print("\nOrder status:")
    print(
        sales_df["order_status"]
        .value_counts()
        .to_string()
    )

    print("\nCategories:")
    print(
        sales_df["category"]
        .value_counts()
        .to_string()
    )

    print("\nSample:")
    print(
        sales_df.head(10).to_string(index=False)
    )

    print("\nDataset generation complete.")