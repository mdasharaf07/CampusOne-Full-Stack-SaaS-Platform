import os
import sys
import logging
from db import execute_query, DatabaseConnection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_tables():
    """
    Reads the full schema from database_full_schema.sql 
    and executes it to initialize the database.
    """
    schema_file = os.path.join(os.path.dirname(__file__), 'database_full_schema.sql')
    
    if not os.path.exists(schema_file):
        logger.error(f"❌ Schema file '{schema_file}' not found.")
        return

    logger.info("🚀 Starting database initialization from live schema...")

    try:
        # Read the SQL file
        with open(schema_file, 'r') as f:
            full_sql = f.read()

        # Split by sections if needed, but executing the whole block is usually fine for Postgres
        # However, we should handle the 'DROP TABLE' logic if we want a clean wipe
        
        drop_queries = """
        DROP TABLE IF EXISTS cultural_bookings CASCADE;
        DROP TABLE IF EXISTS culturals CASCADE;
        DROP TABLE IF EXISTS certificates CASCADE;
        DROP TABLE IF EXISTS attendance CASCADE;
        DROP TABLE IF EXISTS registration_members CASCADE;
        DROP TABLE IF EXISTS registrations CASCADE;
        DROP TABLE IF EXISTS friends CASCADE;
        DROP TABLE IF EXISTS events CASCADE;
        DROP TABLE IF EXISTS users CASCADE;
        DROP TABLE IF EXISTS clubs CASCADE;
        DROP TABLE IF EXISTS halls CASCADE;
        DROP TABLE IF EXISTS refresh_tokens CASCADE;
        DROP TABLE IF EXISTS revoked_tokens CASCADE;
        DROP TABLE IF EXISTS otp_verifications CASCADE;
        DROP TABLE IF EXISTS user_session_history CASCADE;
        """

        with DatabaseConnection() as conn:
            with conn.cursor() as cur:
                logger.info("⏳ Cleaning up existing tables (CASCADE)...")
                cur.execute(drop_queries)
                
                logger.info("⏳ Creating tables, triggers, and seeding data...")
                cur.execute(full_sql)
                
        logger.info("✅ Database is now fully synchronized and ready!")

    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")

if __name__ == "__main__":
    create_tables()
