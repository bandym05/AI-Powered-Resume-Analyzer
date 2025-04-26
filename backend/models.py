from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLITE_DB_URL = "sqlite:///./resumes.db"
engine = create_engine(SQLITE_DB_URL)
Base = declarative_base()

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    skills = Column(String)
    experience = Column(String)
    education = Column(String)
    match_score = Column(Float)
    suggestions = Column(String)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, bind=engine)