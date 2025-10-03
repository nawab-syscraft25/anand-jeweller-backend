#!/usr/bin/env python3
"""
Script to create sample gold rate data for the last 30 days
This will help test the API endpoints and dashboard with realistic data
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine, Base
from models import GoldRate

def create_sample_data():
    """Create sample gold rate data for the last 30 days"""
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        print("Clearing existing gold rate data...")
        db.query(GoldRate).delete()
        db.commit()
        
        print("Creating sample gold rate data for the last 30 days...")
        
        # Base rates (realistic Indian gold prices as of 2025)
        base_24k_selling = 7200.00
        base_24k_exchange = 6800.00
        base_24k_making = 800.00
        
        base_22k_selling = 6600.00
        base_22k_exchange = 6200.00
        base_22k_making = 600.00
        
        base_18k_selling = 5400.00
        base_18k_exchange = 5000.00
        base_18k_making = 400.00
        
        # Create data for last 30 days
        for days_ago in range(30, 0, -1):
            # Calculate the date
            release_date = datetime.now() - timedelta(days=days_ago)
            
            # Add some realistic price variation (±2% daily fluctuation)
            variation_factor = 1 + random.uniform(-0.02, 0.02)
            
            # Create price variations that are somewhat correlated
            trend_factor = 1 + (days_ago - 15) * 0.001  # Slight trend over 30 days
            
            # Calculate rates with variation
            gold_24k_selling = round(base_24k_selling * variation_factor * trend_factor, 2)
            gold_24k_exchange = round(base_24k_exchange * variation_factor * trend_factor, 2)
            gold_24k_making = round(base_24k_making + random.uniform(-50, 50), 2)
            
            gold_22k_selling = round(base_22k_selling * variation_factor * trend_factor, 2)
            gold_22k_exchange = round(base_22k_exchange * variation_factor * trend_factor, 2)
            gold_22k_making = round(base_22k_making + random.uniform(-30, 30), 2)
            
            gold_18k_selling = round(base_18k_selling * variation_factor * trend_factor, 2)
            gold_18k_exchange = round(base_18k_exchange * variation_factor * trend_factor, 2)
            gold_18k_making = round(base_18k_making + random.uniform(-20, 20), 2)
            
            # Set release time to business hours (9 AM to 6 PM)
            release_hour = random.randint(9, 18)
            release_minute = random.choice([0, 15, 30, 45])  # Quarter-hour intervals
            
            release_datetime = release_date.replace(
                hour=release_hour, 
                minute=release_minute, 
                second=0, 
                microsecond=0
            )
            
            # Create consolidated gold rate entry
            gold_rate = GoldRate(
                # 24K Gold rates
                gold_24k_new_rate=gold_24k_selling,
                gold_24k_exchange_rate=gold_24k_exchange,
                gold_24k_making_charges=gold_24k_making,
                
                # 22K Gold rates
                gold_22k_new_rate=gold_22k_selling,
                gold_22k_exchange_rate=gold_22k_exchange,
                gold_22k_making_charges=gold_22k_making,
                
                # 18K Gold rates
                gold_18k_new_rate=gold_18k_selling,
                gold_18k_exchange_rate=gold_18k_exchange,
                gold_18k_making_charges=gold_18k_making,
                
                # Timestamps
                release_datetime=release_datetime,
            )
            
            db.add(gold_rate)
            
            # Print progress
            if days_ago % 5 == 0:
                print(f"Created data for {release_datetime.strftime('%Y-%m-%d %H:%M')} "
                      f"(24K: ₹{gold_24k_selling}, 22K: ₹{gold_22k_selling}, 18K: ₹{gold_18k_selling})")
        
        # Commit all changes
        db.commit()
        
        # Get statistics
        total_records = db.query(GoldRate).count()
        latest_rate = db.query(GoldRate).order_by(GoldRate.release_datetime.desc()).first()
        oldest_rate = db.query(GoldRate).order_by(GoldRate.release_datetime.asc()).first()
        
        print(f"\n✅ Sample data creation completed!")
        print(f"📊 Total records created: {total_records}")
        print(f"📅 Date range: {oldest_rate.release_datetime.strftime('%Y-%m-%d')} to {latest_rate.release_datetime.strftime('%Y-%m-%d')}")
        print(f"💰 Latest rates:")
        print(f"   24K Gold: Selling ₹{latest_rate.gold_24k_new_rate}, Exchange ₹{latest_rate.gold_24k_exchange_rate}, Making ₹{latest_rate.gold_24k_making_charges}")
        print(f"   22K Gold: Selling ₹{latest_rate.gold_22k_new_rate}, Exchange ₹{latest_rate.gold_22k_exchange_rate}, Making ₹{latest_rate.gold_22k_making_charges}")
        print(f"   18K Gold: Selling ₹{latest_rate.gold_18k_new_rate}, Exchange ₹{latest_rate.gold_18k_exchange_rate}, Making ₹{latest_rate.gold_18k_making_charges}")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def create_store_sample_data():
    """Create sample store data"""
    db = SessionLocal()
    
    try:
        from models import Store
        
        # Clear existing stores
        db.query(Store).delete()
        
        # Create sample stores
        stores = [
            Store(
                store_name="Anand Jewels Main Branch",
                store_address="123 MG Road, Commercial Street, Bangalore - 560001",
                store_image="main_store.jpg",
                timings="Monday to Saturday: 10:00 AM - 8:00 PM, Sunday: 11:00 AM - 6:00 PM"
            ),
            Store(
                store_name="Anand Jewels Koramangala",
                store_address="456 Koramangala 4th Block, Bangalore - 560034",
                store_image="koramangala_store.jpg", 
                timings="Monday to Saturday: 10:30 AM - 8:30 PM, Sunday: 11:00 AM - 7:00 PM"
            ),
            Store(
                store_name="Anand Jewels Jayanagar",
                store_address="789 Jayanagar 9th Block, Bangalore - 560069",
                store_image="jayanagar_store.jpg",
                timings="Monday to Saturday: 10:00 AM - 8:00 PM, Sunday: Closed"
            )
        ]
        
        for store in stores:
            db.add(store)
        
        db.commit()
        print(f"✅ Created {len(stores)} sample stores")
        
    except Exception as e:
        print(f"❌ Error creating store data: {str(e)}")
        db.rollback()
    finally:
        db.close()

def create_admin_user():
    """Create sample admin user"""
    db = SessionLocal()
    
    try:
        from models import AdminUser
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Clear existing admin users
        db.query(AdminUser).delete()
        
        # Create admin user (note: using password_hash field name)
        admin_user = AdminUser(
            username="admin",
            password_hash=pwd_context.hash("admin123")  # Default password
        )
        
        db.add(admin_user)
        db.commit()
        
        print("✅ Created admin user (username: admin, password: admin123)")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting sample data creation...")
    print("=" * 50)
    
    # Create all sample data
    create_sample_data()
    create_store_sample_data() 
    create_admin_user()
    
    print("=" * 50)
    print("🎉 All sample data created successfully!")
    print("\n📝 You can now test the following:")
    print("1. Dashboard: http://localhost:8000/admin")
    print("2. API Latest: http://localhost:8000/api/gold-rates/latest")
    print("3. API History: http://localhost:8000/api/gold-rates/history/7d")
    print("4. API Current: http://localhost:8000/api/gold-rates/current")
    print("5. Login with: username=admin, password=admin123")