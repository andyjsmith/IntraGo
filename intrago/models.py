from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import db


class Site(db.Model):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    url = Column(String)
    prefixed = Column(Boolean)
    created = Column(DateTime())
    accesses = Column(Integer, default=0)

    def __init__(self, name, url, prefixed):
        self.name = name
        self.url = url
        self.prefixed = prefixed
        self.created = datetime.utcnow()
