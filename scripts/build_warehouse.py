from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MARTS_DIR = BASE_DIR / "data" / "marts"

DB_PATH = BASE_DIR / "product_intelligence.duckdb"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MARTS_DIR.mkdir(parents=True, exist_ok=True)

conn = duckdb.connect(DB_PATH)

# Load raw events
conn.execute(f"""
    CREATE OR REPLACE TABLE raw_events AS
    SELECT *
    FROM read_parquet('{RAW_DIR / "product_events.parquet"}');
""")

print("Raw events loaded.")

# Staging layer
conn.execute("""
    CREATE OR REPLACE TABLE stg_events AS
    SELECT
        event_id,
        user_id,
        event_type,
        platform,
        country,
        revenue,
        CAST(event_timestamp AS TIMESTAMP) AS event_timestamp,
        DATE_TRUNC('month', event_timestamp) AS event_month
    FROM raw_events;
""")

print("Staging layer created.")

# Revenue mart
conn.execute("""
    CREATE OR REPLACE TABLE mart_revenue AS
    SELECT
        event_month,
        country,
        platform,
        COUNT(*) AS total_events,
        COUNT(DISTINCT user_id) AS active_users,
        SUM(revenue) AS total_revenue,
        AVG(revenue) AS avg_revenue_per_event
    FROM stg_events
    GROUP BY 1,2,3
    ORDER BY 1;
""")

print("Revenue mart created.")

# Funnel mart
conn.execute("""
    CREATE OR REPLACE TABLE mart_funnel AS
    SELECT
        event_type,
        COUNT(*) AS total_events,
        COUNT(DISTINCT user_id) AS unique_users
    FROM stg_events
    GROUP BY 1
    ORDER BY total_events DESC;
""")

print("Funnel mart created.")

# Export marts
conn.execute(f"""
    COPY mart_revenue
    TO '{MARTS_DIR / "mart_revenue.csv"}'
    (HEADER, DELIMITER ',');
""")

conn.execute(f"""
    COPY mart_funnel
    TO '{MARTS_DIR / "mart_funnel.csv"}'
    (HEADER, DELIMITER ',');
""")

print("Marts exported successfully.")

conn.close()

print(f"Warehouse available at: {DB_PATH}")