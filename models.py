"""
This module is used to establish database
connection and modules. Very simple for this
project due to the nature of it being very small.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Request(Base):
    """
    This class structures the requests table.
    This table is used for recording and tracking
    all requests to connect over SSH.
    """
    __tablename__ = 'requests'

    req_id = Column(Integer, primary_key=True)
    msg_id = Column(Integer)
    user = Column(String)
    host = Column(String)
    remote = Column(String)
    decision = Column(String)
    decider = Column(String)
    request_ts = Column(DateTime)
    decision_ts = Column(DateTime)

    def __repr__(self):
        """
        This function returns a human-readable representation of the object.
        """
        return f"Request(<reqid={self.reqid}, msg_id={self.msg_id}, user='{self.user}', host='{self.host}', remote='{self.remote}', decision='{self.decision}', decider='{self.decider}', request_ts={self.request_ts}, decision_ts={self.decision_ts}>)"

def init_db(db_uri: str) -> None:
    """
    This function will initialize the database.
    """
    from sqlalchemy import create_engine
    engine = create_engine(db_uri)
    Base.metadata.create_all(bind=engine)
    return None

if __name__ == "__main__":
    import sys
    print("This module should only be imported.")
    sys.exit(1)