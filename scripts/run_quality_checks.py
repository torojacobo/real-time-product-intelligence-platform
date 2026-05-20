from pathlib import Path
import duckdb
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "product_intelligence.duckdb"
MARTS_DIR = BASE_DIR / "data" / "marts"

conn = duckdb.connect(DB_PATH)

quality_results = []

checks = [

    {
        "check_name": "null_event_ids",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE event_id IS NULL;
        """
    },

    {
        "check_name": "null_user_ids",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE user_id IS NULL;
        """
    },

    {
        "check_name": "invalid_event_types",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE event_type NOT IN (
                'app_open',
                'product_view',
                'add_to_cart',
                'purchase',
                'refund'
            );
        """
    },

    {
        "check_name": "negative_purchase_revenue",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE event_type = 'purchase'
            AND revenue < 0;
        """
    },

    {
        "check_name": "positive_refund_revenue",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE event_type = 'refund'
            AND revenue > 0;
        """
    },

    {
        "check_name": "future_events",
        "query": """
            SELECT COUNT(*) AS failed_records
            FROM stg_events
            WHERE event_timestamp > CURRENT_TIMESTAMP;
        """
    }

]

for check in checks:

    failed_records = conn.execute(
        check["query"]
    ).fetchone()[0]

    status = (
        "passed"
        if failed_records == 0
        else "failed"
    )

    quality_results.append({
        "check_name": check["check_name"],
        "failed_records": failed_records,
        "status": status
    })

quality_df = pd.DataFrame(quality_results)

output_path = MARTS_DIR / "quality_check_results.csv"

quality_df.to_csv(output_path, index=False)

print("\nQuality checks completed.")
print(quality_df)

conn.close()