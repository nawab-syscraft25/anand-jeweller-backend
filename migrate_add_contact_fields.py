#!/usr/bin/env python3
"""
Migration script to add no_of_people and message fields to contact_enquiries table
"""

import sqlite3
from datetime import datetime

def migrate_database():
    """Add new fields to contact_enquiries table"""
    
    # Connect to the database
    conn = sqlite3.connect('gold_rates.db')
    cursor = conn.cursor()
    
    try:
        print("🔄 Starting migration: Adding no_of_people and message fields to contact_enquiries...")
        
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(contact_enquiries)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add no_of_people column if it doesn't exist
        if 'no_of_people' not in columns:
            cursor.execute("""
                ALTER TABLE contact_enquiries 
                ADD COLUMN no_of_people INTEGER DEFAULT 1
            """)
            print("✅ Added no_of_people column")
        else:
            print("ℹ️  no_of_people column already exists")
        
        # Add message column if it doesn't exist
        if 'message' not in columns:
            cursor.execute("""
                ALTER TABLE contact_enquiries 
                ADD COLUMN message TEXT DEFAULT 'NaN'
            """)
            print("✅ Added message column")
        else:
            print("ℹ️  message column already exists")
        
        # Commit the changes
        conn.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(contact_enquiries)")
        columns_after = cursor.fetchall()
        print("\n📋 Current contact_enquiries table structure:")
        for column in columns_after:
            print(f"   - {column[1]} ({column[2]}) {'NOT NULL' if column[3] else 'NULL'} DEFAULT: {column[4] or 'None'}")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()