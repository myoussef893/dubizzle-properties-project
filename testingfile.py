from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data.db')


Base = declarative_base()

class User(Base): 
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    email =Column(String)

Base.metadata.create_all(engine)

# Create a session to manage database interactions

Session = sessionmaker(bind=engine)

session = Session()



# Add a user to the database

user = User(name='John Doe', email='johndoe@example.com')

session.add(user)

session.commit()



# Query for users

users = session.query(User).all()

print(user)

