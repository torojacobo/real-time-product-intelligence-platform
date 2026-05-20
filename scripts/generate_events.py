from faker import Faker
import pandas as pd
import random
from pathlib import Path

fake = Faker()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

EVENT_TYPES = [
    "app_open",
    "product_view",
    "add_to_cart",
    "purchase",
    "refund"
]

PLATFORMS = [
    "iOS",
    "Android",
    "Web"
]

COUNTRIES = [
    "Mexico",
    "USA",
    "Colombia",
    "Brazil"
]

events = []

for _ in range(5000):

    event_type = random.choice(EVENT_TYPES)

    revenue = 0

    if event_type == "purchase":
        revenue = round(random.uniform(10, 500), 2)

    if event_type == "refund":
        revenue = -round(random.uniform(5, 200), 2)

    events.append({
        "event_id": fake.uuid4(),
        "user_id": random.randint(1000, 5000),
        "event_type": event_type,
        "platform": random.choice(PLATFORMS),
        "country": random.choice(COUNTRIES),
        "revenue": revenue,
        "event_timestamp": fake.date_time_this_year()
    })

df = pd.DataFrame(events)

output_path = RAW_DIR / "product_events.parquet"

df.to_parquet(output_path, index=False)

print("Events generated successfully.")
print(f"Output: {output_path}")
print(f"Rows: {len(df)}")