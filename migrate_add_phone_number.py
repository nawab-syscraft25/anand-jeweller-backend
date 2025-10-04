#!/usr/bin/env python3
"""
Migration script to add phone_number column to stores table
Run this script to update your database schema
"""

import sqlite3
import os
from pathlib import Path

def add_phone_number_column():
    """Add phone_number column to stores table"""
    
    # Database file path
    db_path = Path(__file__).parent / "gold_rates.db"
    
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(stores)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'phone_number' in columns:
            print("Column 'phone_number' already exists in stores table")
            return True
        
        # Add the phone_number column
        cursor.execute("ALTER TABLE stores ADD COLUMN phone_number TEXT")
        
        # Commit changes
        conn.commit()
        print("Successfully added 'phone_number' column to stores table")
        
        # Verify the column was added
        cursor.execute("PRAGMA table_info(stores)")
        columns_after = [column[1] for column in cursor.fetchall()]
        print(f"Stores table columns: {columns_after}")
        
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

def add_new_tables():
    """Add new tables: about, team, missions, terms"""
    
    db_path = Path(__file__).parent / "gold_rates.db"
    
    if not db_path.exists():
        print(f"Database file not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create about table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS about (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create team table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS team (
                id INTEGER PRIMARY KEY,
                position TEXT NOT NULL,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create missions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create terms table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS terms (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("Successfully created new tables: about, team, missions, terms")
        return True
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("Running database migration...")
    print("=" * 50)
    
    # Add phone_number column to stores table
    success1 = add_phone_number_column()
    
    # Add new tables
    success2 = add_new_tables()
    
    if success1 and success2:
        print("\n✅ Migration completed successfully!")
        print("You can now restart your application.")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
