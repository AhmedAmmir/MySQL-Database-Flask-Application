from tables import Base
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

class MySQLSession():

    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        
        self.url: str = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
        self.engine: Engine = create_engine(self.url)
        self.sessionMaker: sessionmaker = sessionmaker(self.engine)

    def session_is_connected(self) -> bool:
        
        with self.sessionMaker.begin() as session:
            
            try:
                session.execute(
                    text("SELECT 1")
                )
            except OperationalError as err:
                print("Failure")
                raise err
        
        print("Success")

        return True

    def session_insert_one(self, record: Base) -> None:
        
        with self.sessionMaker.begin() as session:
            session.add(record)
    
    def session_insert_many(self, recordList: list[Base]):
        
        with self.sessionMaker.begin() as session:
            
            for record in recordList:
                session.add(record)