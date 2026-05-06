from pipelines.db import get_connection
from pipelines.extract import fetch_weather
from pipelines.transform import transform_weather
from pipelines.load import upsert_weather
from pipelines.checkpoints import get_last_checkpoint, update_checkpoint
from pipelines.run_history import log_run

import datetime


def run_pipeline():
    conn = get_connection()

    try:
        city = "Bangalore"
        latitude = 12.9716
        longitude = 77.5946

        today = datetime.date.today()

        # 🔹 Check last checkpoint
        last_checkpoint = get_last_checkpoint(conn)

        if last_checkpoint:
            # Incremental load
            start_date = last_checkpoint + datetime.timedelta(days=1)
            print(f"Running incremental load from {start_date}")
        else:
            # Baseline load (last 30 days)
            start_date = today - datetime.timedelta(days=30)
            print(f"Running baseline load from {start_date}")

        end_date = today
        if start_date > end_date:
            print("No new data to process.")
            log_run(conn, "NO_NEW_DATA")
            return

        # 🔹 Extract
        raw_data = fetch_weather(
            latitude,
            longitude,
            start_date.isoformat(),
            end_date.isoformat()
        )

        # 🔹 Transform
        df = transform_weather(raw_data, city)

        # 🔹 Load (UPSERT)
        upsert_weather(conn, df)

        # 🔹 Update checkpoint
        update_checkpoint(conn, end_date)

        # 🔹 Log success
        log_run(conn, "SUCCESS")
        conn.commit()

        print("Pipeline completed successfully!")

    except Exception as e:
        conn.rollback()
        log_run(conn, "FAILED")
        print("Pipeline failed:", e)

    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline()