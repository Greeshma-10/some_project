"""
Load weather data into Supabase Postgres.
"""

def upsert_weather(conn, df):
    """
    Insert or update weather records using UPSERT.
    """

    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO weather_data (city, date, temp_max, temp_min)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (city, date)
            DO UPDATE SET
                temp_max = EXCLUDED.temp_max,
                temp_min = EXCLUDED.temp_min;
        """, (
            row["city"],
            row["date"],
            row["temp_max"],
            row["temp_min"]
        ))
