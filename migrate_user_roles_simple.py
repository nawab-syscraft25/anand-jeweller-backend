#!/usr/bin/env python3
"""
Simple migration to add user roles using existing database connection
"""

import sys
import os
import sqlite3
from pathlib import Path

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def migrate_add_user_roles():
    """Add user roles using direct SQLite connection"""
    
    print("🚀 Starting user roles migration...")
    
    # Get database path
    db_path = Path("gold_rates.db")
    
    if not db_path.exists():
        print("❌ Database file not found. Please run the main application first.")
        return
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Check if role column already exists
        cursor.execute("PRAGMA table_info(admin_users);")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'role' in columns:
            print("✅ Role column already exists")
        else:
            print("📝 Adding role column to admin_users table...")
            cursor.execute("""
                ALTER TABLE admin_users 
                ADD COLUMN role VARCHAR(20) DEFAULT 'super_admin' NOT NULL;
            """)
            
        if 'created_at' not in columns:
            print("📝 Adding created_at column to admin_users table...")
            cursor.execute("""
                ALTER TABLE admin_users 
                ADD COLUMN created_at DATETIME;
            """)
            # Update existing records with current timestamp
            cursor.execute("""
                UPDATE admin_users 
                SET created_at = CURRENT_TIMESTAMP 
                WHERE created_at IS NULL;
            """)
        
        # Update existing users to have super_admin role
        print("👑 Setting existing users as Super Admin...")
        cursor.execute("""
            UPDATE admin_users 
            SET role = 'super_admin' 
            WHERE role IS NULL OR role = '' OR role = 'super_admin';
        """)
        
        # Check if contact_manager user exists
        cursor.execute("SELECT COUNT(*) FROM admin_users WHERE username = 'contact_manager';")
        user_exists = cursor.fetchone()[0]
        
        if user_exists == 0:
            print("👤 Creating sample Contact Manager user...")
            
            # Create bcrypt hash for password 'contact123'
            import bcrypt
            password = "contact123"
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            cursor.execute("""
                INSERT INTO admin_users (username, password_hash, role, created_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP);
            """, ("contact_manager", hashed_password, "contact_manager"))
            
            print("✅ Created contact manager user (username: contact_manager, password: contact123)")
        else:
            print("ℹ️  Contact manager user already exists")
            # Update existing contact_manager to have correct role
            cursor.execute("""
                UPDATE admin_users 
                SET role = 'contact_manager' 
                WHERE username = 'contact_manager';
            """)
        
        # Commit changes
        conn.commit()
        
        # Verify migration
        cursor.execute("SELECT username, role, created_at FROM admin_users ORDER BY created_at;")
        users = cursor.fetchall()
        
        print("\n📊 Current users after migration:")
        for user in users:
            created_at = user[2] if user[2] else 'Unknown'
            print(f"  - {user[0]}: {user[1]} (created: {created_at})")
        
        print("\n✅ User roles migration completed successfully!")
        print("\n🔑 Login credentials:")
        print("   Super Admin - username: admin, password: admin123")  
        print("   Contact Manager - username: contact_manager, password: contact123")
        print("\n📋 Role-based access:")
        print("   ✓ Super Admin: Full access to all modules")
        print("   ✓ Contact Manager: Access only to Contact Enquiries")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    migrate_add_user_roles()