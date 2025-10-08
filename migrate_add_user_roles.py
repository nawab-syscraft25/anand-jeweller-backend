#!/usr/bin/env python3
"""
Migration script to add user roles using SQLAlchemy ORM
"""

import sys
import os
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base
from models import AdminUser, UserRole

def migrate_add_user_roles():
    """Create updated tables and migrate existing data using ORM"""
    
    print("🚀 Starting user roles migration using SQLAlchemy ORM...")
    
    try:
        # Create all tables with new schema (this will add new columns)
        print("📝 Creating/updating database schema...")
        Base.metadata.create_all(bind=engine)
        
        # Create database session
        db = SessionLocal()
        
        try:
            # Check if we have any existing users
            existing_users = db.query(AdminUser).all()
            
            # Update existing users to have super_admin role if they don't have a role
            print("� Setting existing users as Super Admin...")
            for user in existing_users:
                if not hasattr(user, 'role') or user.role is None:
                    user.role = UserRole.SUPER_ADMIN
                    print(f"  - Updated user '{user.username}' to Super Admin")
            
            # Check if we need to create sample contact manager user
            contact_manager = db.query(AdminUser).filter(
                AdminUser.username == "contact_manager"
            ).first()
            
            if not contact_manager:
                print("👤 Creating sample Contact Manager user...")
                
                # Import bcrypt for password hashing (matching existing auth system)
                import bcrypt
                
                # Hash password using bcrypt (matching existing system)
                password = "contact123"
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Create contact manager user
                contact_manager = AdminUser(
                    username="contact_manager",
                    password_hash=hashed_password,
                    role=UserRole.CONTACT_MANAGER,
                    created_at=datetime.now()
                )
                
                db.add(contact_manager)
                print("✅ Created contact manager user (username: contact_manager, password: contact123)")
            else:
                print("ℹ️  Contact manager user already exists")
                # Make sure existing contact_manager has correct role
                if contact_manager.role != UserRole.CONTACT_MANAGER:
                    contact_manager.role = UserRole.CONTACT_MANAGER
                    print("  - Updated existing contact_manager to have correct role")
            
            # Commit all changes
            db.commit()
            
            # Verify migration by listing all users
            print("\n📊 Current users after migration:")
            all_users = db.query(AdminUser).order_by(AdminUser.created_at).all()
            
            for user in all_users:
                created_at = user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'Unknown'
                print(f"  - {user.username}: {user.role.value} (created: {created_at})")
        
            print("\n✅ User roles migration completed successfully!")
            print("\n🔑 Login credentials:")
            print("   Super Admin - username: admin, password: admin123")
            print("   Contact Manager - username: contact_manager, password: contact123")
            print("\n📋 Features:")
            print("   ✓ Super Admin: Full access to all modules")
            print("   ✓ Contact Manager: Access only to Contact Enquiries")
            
        except Exception as e:
            print(f"❌ Database operation failed: {str(e)}")
            db.rollback()
            raise
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    migrate_add_user_roles()