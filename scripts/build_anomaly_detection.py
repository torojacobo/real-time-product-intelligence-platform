from pathlib import Path
import duckdb

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "product_intelligence.duckdb"
MARTS_DIR = BASE_DIR / "data" / "marts"

conn = duckdb.connect(DB_PATH)

conn.execute("""

CREATE OR REPLACE TABLE mart_anomalies AS

WITH monthly_revenue AS (

    SELECT
        DATE_TRUNC('month', event_timestamp) AS event_month,
        SUM(revenue) AS total_revenue

    FROM stg_events

    GROUP BY 1

),

stats AS (

    SELECT
        AVG(total_revenue) AS avg_revenue,
        STDDEV(total_revenue) AS std_revenue

    FROM monthly_revenue

)

SELECT
    mr.event_month,
    mr.total_revenue,
    s.avg_revenue,
    s.std_revenue,

    ABS(
        mr.total_revenue - s.avg_revenue
    ) AS deviation,

    CASE
        WHEN ABS(
            mr.total_revenue - s.avg_revenue
        ) > (2 * s.std_revenue)
        THEN 'anomaly'

        ELSE 'normal'
    END AS anomaly_status

FROM monthly_revenue mr
CROSS JOIN stats s

ORDER BY mr.event_month;

""")

conn.execute(f"""
    COPY mart_anomalies
    TO '{MARTS_DIR / "mart_anomalies.csv"}'
    (HEADER, DELIMITER ',');
""")

print("Anomaly detection mart created successfully.")

conn.close()