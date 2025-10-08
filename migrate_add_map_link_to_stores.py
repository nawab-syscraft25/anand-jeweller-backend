#!/usr/bin/env python3
"""
Migration script to add map_link column to stores table
This handles SQLite constraints by creating a new table and copying data
"""

import sqlite3
import os
from datetime import datetime

def migrate_add_map_link():
    """Add map_link column to stores table with SQLite-compatible approach"""
    
    db_path = "gold_rates.db"
    
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found!")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("Starting migration: Adding map_link column to stores table...")
        
        # Check if map_link column already exists
        cursor.execute("PRAGMA table_info(stores)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'map_link' in columns:
            print("✅ map_link column already exists in stores table")
            conn.close()
            return True
        
        print("📋 Current stores table columns:", ", ".join(columns))
        
        # Step 1: Create new stores table with map_link column
        print("📝 Creating new stores table with map_link column...")
        cursor.execute("""
        CREATE TABLE stores_new (
            id INTEGER PRIMARY KEY,
            store_name VARCHAR NOT NULL,
            phone_number VARCHAR,
            store_address TEXT NOT NULL,
            store_image VARCHAR,
            youtube_link VARCHAR,
            map_link VARCHAR DEFAULT 'Na',
            timings VARCHAR NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Step 2: Copy all data from old table to new table
        print("📊 Copying existing store data...")
        cursor.execute("""
        INSERT INTO stores_new (
            id, store_name, phone_number, store_address, 
            store_image, youtube_link, timings, created_at
        )
        SELECT 
            id, store_name, phone_number, store_address,
            store_image, youtube_link, timings, created_at
        FROM stores
        """)
        
        # Get count of copied records
        cursor.execute("SELECT COUNT(*) FROM stores_new")
        new_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM stores")
        old_count = cursor.fetchone()[0]
        
        print(f"📈 Copied {new_count} records (original: {old_count})")
        
        if new_count != old_count:
            print("❌ Data copy mismatch! Rolling back...")
            conn.rollback()
            conn.close()
            return False
        
        # Step 3: Drop old table and rename new table
        print("🔄 Replacing old table with new table...")
        cursor.execute("DROP TABLE stores")
        cursor.execute("ALTER TABLE stores_new RENAME TO stores")
        
        # Step 4: Verify the migration
        print("✅ Verifying migration...")
        cursor.execute("PRAGMA table_info(stores)")
        new_columns = [column[1] for column in cursor.fetchall()]
        
        if 'map_link' not in new_columns:
            print("❌ Migration verification failed!")
            conn.rollback()
            conn.close()
            return False
        
        # Commit all changes
        conn.commit()
        
        print("📋 New stores table columns:", ", ".join(new_columns))
        print("✅ Migration completed successfully!")
        
        # Show sample of new data structure
        cursor.execute("SELECT id, store_name, map_link FROM stores LIMIT 3")
        sample_data = cursor.fetchall()
        
        print("\n📋 Sample data verification:")
        for row in sample_data:
            print(f"  Store ID {row[0]}: {row[1]} - Map Link: {row[2]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MIGRATION: Add map_link column to stores table")
    print("=" * 60)
    
    success = migrate_add_map_link()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("💡 You can now restart your server - the map_link field is ready to use.")
    else:
        print("\n💥 Migration failed!")
        print("🔧 Please check the error messages above and try again.")
    
    print("=" * 60)