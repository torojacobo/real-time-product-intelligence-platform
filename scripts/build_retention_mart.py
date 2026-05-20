from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "product_intelligence.duckdb"
MARTS_DIR = BASE_DIR / "data" / "marts"

conn = duckdb.connect(DB_PATH)

conn.execute("""
    CREATE OR REPLACE TABLE mart_retention AS

    WITH monthly_users AS (

        SELECT
            user_id,
            DATE_TRUNC('month', event_timestamp) AS event_month
        FROM stg_events
        GROUP BY 1,2

    ),

    user_activity AS (

        SELECT
            current_month.user_id,
            current_month.event_month,

            CASE
                WHEN previous_month.user_id IS NOT NULL
                THEN 1
                ELSE 0
            END AS retained_user

        FROM monthly_users current_month

        LEFT JOIN monthly_users previous_month
            ON current_month.user_id = previous_month.user_id
            AND current_month.event_month =
                previous_month.event_month + INTERVAL '1 month'

    )

    SELECT
        event_month,

        COUNT(DISTINCT user_id) AS monthly_active_users,

        SUM(retained_user) AS returning_users,

        ROUND(
            SUM(retained_user) * 1.0
            / COUNT(DISTINCT user_id),
            4
        ) AS retention_rate

    FROM user_activity

    GROUP BY 1
    ORDER BY 1;
""")

conn.execute(f"""
    COPY mart_retention
    TO '{MARTS_DIR / "mart_retention.csv"}'
    (HEADER, DELIMITER ',');
""")

print("Retention mart created successfully.")

conn.close()