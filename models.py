from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint, Text
from sqlalchemy.sql import func
from database import Base

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

class GoldRate(Base):
    __tablename__ = "gold_rates"
    
    id = Column(Integer, primary_key=True, index=True)
    purity = Column(String, nullable=False)  # "24K", "22K", "18K"
    new_rate_per_gram = Column(Float, nullable=False)
    old_rate_per_gram = Column(Float, nullable=False)
    release_datetime = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Ensure no duplicate entries for same purity + release_datetime
    __table_args__ = (
        UniqueConstraint('purity', 'release_datetime', name='_purity_release_datetime_uc'),
    )
    
    def __repr__(self):
        return f"<GoldRate(purity='{self.purity}', new_rate={self.new_rate_per_gram}, release_datetime='{self.release_datetime}')>"


class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    store_address = Column(Text, nullable=False)
    store_image = Column(String, nullable=True)  # Path to store image
    timings = Column(String, nullable=False)  # e.g., "Mon-Sat: 10:00 AM - 8:00 PM, Sun: 11:00 AM - 6:00 PM"
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Store(name='{self.store_name}', address='{self.store_address}')>"


class ContactEnquiry(Base):
    __tablename__ = "contact_enquiries"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=False)
    preferred_store = Column(String, nullable=False)
    preferred_date_time = Column(String, nullable=False)  # Stored as string as requested
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<ContactEnquiry(name='{self.name}', phone='{self.phone_number}', preferred_store='{self.preferred_store}')>"


class Guide(Base):
    __tablename__ = "guides"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Guide(title='{self.title}', image='{self.image}')>"