from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
Base = declarative_base()

class TikTokAccount(Base):
    __tablename__ = "tiktok_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)

    username = Column(String)
    email = Column(String)
    password = Column(String)
    
    token = Column(String)

    status = Column(String)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}