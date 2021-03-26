from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///C:\\sqlite\\newFasApi.db',echo= True)
SessionLocal = sessionmaker(autocommit= False , autoflush=False, bind=engine)
Base = declarative_base()
#Me = User(lname= 'Boet' , fname= 'Pedro' , email= 'cojones@gmail.com')
#session.add(Me)
#session.commit()
