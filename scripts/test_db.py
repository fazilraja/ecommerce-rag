from app.config.settings import get_settings
import psycopg
from typing import NoReturn
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./app/.env")
def test_db_connection() -> NoReturn:
    """Test the database connection using settings from config."""
    settings = get_settings()
    print(f"Service URL: {settings.database.service_url}")
    print(f"Environment URL: {os.getenv('TIMESCALE_SERVICE_URL')}")
    
    try:
        with psycopg.connect(settings.database.service_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                print("Successfully connected to TimescaleDB!")
                print(f"Server version: {version[0]}")
    except Exception as e:
        print(f"Connection failed: {str(e)}")

if __name__ == "__main__":
    test_db_connection()