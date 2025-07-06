from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to user reports
    reports = relationship("UserReport", back_populates="user")


class UserReport(Base):
    __tablename__ = 'user_reports'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    jobs_data = Column(Text, nullable=False)  # JSON string of scraped jobs
    keyword = Column(String(255))  # Search keyword used
    sources_used = Column(Text)  # JSON string of source IDs used
    job_count = Column(Integer, default=0)  # Number of jobs in the report
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to user
    user = relationship("User", back_populates="reports")


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    base_url = Column(String(512), nullable=False)


class JobPosting(Base):
    __tablename__ = 'job_postings'

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    company = Column(String(512))
    location = Column(String(512))
    salary = Column(String(255))
    date_posted = Column(String(255))
    description = Column(Text)
    url = Column(String(1024))
    source_id = Column(Integer, ForeignKey('sources.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
