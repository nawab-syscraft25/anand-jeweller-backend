"""
Database migration script to add making_charges column to gold_rates table
"""
from sqlalchemy import text
from database import engine

def migrate_database():
    """Add making_charges column to existing gold_rates table"""
    try:
        with engine.connect() as connection:
            # Check if making_charges column exists
            result = connection.execute(text("""
                SELECT COUNT(*) 
                FROM pragma_table_info('gold_rates') 
                WHERE name='making_charges'
            """))
            
            column_exists = result.scalar() > 0
            
            if not column_exists:
                print("Adding making_charges column to gold_rates table...")
                connection.execute(text("""
                    ALTER TABLE gold_rates 
                    ADD COLUMN making_charges FLOAT NOT NULL DEFAULT 0.0
                """))
                connection.commit()
                print("✅ Successfully added making_charges column")
            else:
                print("✅ making_charges column already exists")
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        
if __name__ == "__main__":
    migrate_database()