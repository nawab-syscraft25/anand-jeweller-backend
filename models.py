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
    
    # 24K Gold Rates
    gold_24k_new_rate = Column(Float, nullable=False)  # 24K selling price per gram
    gold_24k_exchange_rate = Column(Float, nullable=False)  # 24K exchange price per gram
    gold_24k_making_charges = Column(Float, nullable=False, default=0.0)  # 24K making charges per gram
    
    # 22K Gold Rates
    gold_22k_new_rate = Column(Float, nullable=False)  # 22K selling price per gram
    gold_22k_exchange_rate = Column(Float, nullable=False)  # 22K exchange price per gram
    gold_22k_making_charges = Column(Float, nullable=False, default=0.0)  # 22K making charges per gram
    
    # 18K Gold Rates
    gold_18k_new_rate = Column(Float, nullable=False)  # 18K selling price per gram
    gold_18k_exchange_rate = Column(Float, nullable=False)  # 18K exchange price per gram
    gold_18k_making_charges = Column(Float, nullable=False, default=0.0)  # 18K making charges per gram
    
    release_datetime = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Ensure no duplicate entries for same release_datetime
    __table_args__ = (
        UniqueConstraint('release_datetime', name='_release_datetime_uc'),
    )
    
    def __repr__(self):
        return f"<GoldRate(24K: ₹{self.gold_24k_new_rate}, 22K: ₹{self.gold_22k_new_rate}, 18K: ₹{self.gold_18k_new_rate}, released: {self.release_datetime})>"


class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    store_address = Column(Text, nullable=False)
    store_image = Column(String, nullable=True)  # URL/Path to store image
    youtube_link = Column(String, nullable=True)  # YouTube video link
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

class About(Base):
    __tablename__ = "about"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<About(title='{self.title}', image='{self.image}')>"
    
class Team(Base):
    __tablename__ = "team"
    
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String, nullable=False)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Team(name='{self.name}', position='{self.position}')>"

class Mission(Base):
    __tablename__ = "missions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Mission(title='{self.title}', image='{self.image}')>"

class Terms(Base):
    __tablename__ = "terms"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Terms(title='{self.title}', image='{self.image}')>"

class Vision(Base):
    __tablename__ = "visions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Vision(title='{self.title}', image='{self.image}')>"

class Award(Base):
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Award(title='{self.title}')>"

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)  # Achievement date
    content = Column(Text, nullable=False)
    image = Column(String, nullable=True)  # Path to uploaded image
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Achievement(title='{self.title}', date='{self.date}')>"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    datetime = Column(DateTime, nullable=False)  # Notification date and time
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Notification(title='{self.title}', datetime='{self.datetime}')>"
    

