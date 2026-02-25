import os
import sys
import psycopg2
from dotenv import load_dotenv

def extract_schema():
    """
    Connects to the Neon database and extracts the full schema 
    (tables, constraints, triggers) to recreate the system.
    """
    # Load environment variables with absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, '.env')
    load_dotenv(env_path)
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("❌ Error: DATABASE_URL not found in .env")
        return

    print(f"🚀 Connecting to database to extract schema...")
    
    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        schema_content = [
            "-- ==========================================",
            "-- CampusHub Extracted Database Schema",
            f"-- Extracted on: {psycopg2.TimestampFromTicks(0)}",
            "-- ==========================================\n"
        ]

        # 1. Get all tables in public schema
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = [t[0] for t in cur.fetchall()]

        # 2. Extract Table Definitions
        for table in tables:
            print(f"📦 Extracting table: {table}")
            schema_content.append(f"-- Table: {table}")
            schema_content.append(f"CREATE TABLE IF NOT EXISTS {table} (")
            
            # Get Columns
            cur.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table}'
                ORDER BY ordinal_position;
            """)
            columns = cur.fetchall()
            
            col_defs = []
            for col in columns:
                name, dtype, nullable, default = col
                # Map data types if necessary (e.g., character varying -> VARCHAR)
                type_str = dtype.upper()
                if type_str == "CHARACTER VARYING": type_str = "VARCHAR"
                
                null_str = "NOT NULL" if nullable == "NO" else ""
                
                # Handle defaults (sequences, etc)
                def_str = ""
                if default:
                    if "nextval" in default:
                        # Use SERIAL if it's a sequence default
                        if name == "id":
                            type_str = "SERIAL"
                            def_str = ""
                        else:
                            def_str = f"DEFAULT {default}"
                    else:
                        def_str = f"DEFAULT {default}"
                
                col_defs.append(f"    {name} {type_str} {null_str} {def_str}".strip())
            
            # Get Primary Key
            cur.execute(f"""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = '{table}'::regclass
                AND i.indisprimary;
            """)
            pk = cur.fetchone()
            if pk:
                col_defs.append(f"    PRIMARY KEY ({pk[0]})")

            # Get Foreign Keys
            cur.execute(f"""
                SELECT
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.key_column_usage AS kcu 
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = kcu.constraint_name
                WHERE kcu.table_name = '{table}' AND kcu.constraint_name LIKE '%_fkey';
            """)
            fkeys = cur.fetchall()
            for fk in fkeys:
                col_defs.append(f"    FOREIGN KEY ({fk[0]}) REFERENCES {fk[1]}({fk[2]}) ON DELETE SET NULL")

            # Get Unique Constraints (excluding PK)
            cur.execute(f"""
                SELECT column_name
                FROM information_schema.key_column_usage kcu
                JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'UNIQUE' AND kcu.table_name = '{table}';
            """)
            uniques = cur.fetchall()
            for u in uniques:
                col_defs.append(f"    UNIQUE ({u[0]})")

            schema_content.append(",\n".join(col_defs))
            schema_content.append(");\n")

        # 3. Get Triggers and Functions
        print("⚡ Extracting Triggers and Functions...")
        cur.execute("""
            SELECT 
                p.proname as function_name,
                pg_get_functiondef(p.oid) as function_def
            FROM pg_proc p
            JOIN pg_namespace n ON p.pronamespace = n.oid
            WHERE n.nspname = 'public'
            AND p.prokind = 'f';
        """)
        functions = cur.fetchall()
        for func_name, func_def in functions:
            schema_content.append(f"-- Function: {func_name}")
            schema_content.append(func_def.strip() + ";\n")

        cur.execute("""
            SELECT 
                tgname as trigger_name,
                pg_get_triggerdef(t.oid) as trigger_def
            FROM pg_trigger t
            WHERE t.tgisinternal = false;
        """)
        triggers = cur.fetchall()
        for tg_name, tg_def in triggers:
            schema_content.append(f"-- Trigger: {tg_name}")
            schema_content.append(tg_def.strip() + ";\n")

        # 4. Save to SQL file
        output_file = 'backend/database_full_schema.sql'
        print(f"💾 Saving to {output_file}...")
        with open(output_file, 'w') as f:
            f.write("\n".join(schema_content))
        
        print(f"✅ Schema extracted successfully!")
        sys.stdout.flush()

        cur.close()
        conn.close()

    except Exception as e:
        print(f"💥 Error during extraction: {e}")

if __name__ == "__main__":
    extract_schema()
