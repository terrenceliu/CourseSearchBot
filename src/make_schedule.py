from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

# CATALOG_FILE = 'data/engineering_schedule.csv'
ENGI_SCHEDULE_FILE = './data/engi_schedule.csv'

"""
	Configuration
"""
Base = declarative_base()
engine = create_engine('postgresql://localhost/catalog', echo=True)
# start session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Schedule(Base):
	__tablename__ = 'course'
	id = Column(Integer, primary_key=True)
	crn = Column(String)
	course_code = Column(String)
	session = Column(String)
	title = Column(String)
	instructor = Column(String)
	schedule = Column(String)
	credits = Column(String)
	
	
	def __repr__(self):
		"""
		Define the representation of the database.
		:return:
		"""
		return "<Course(courde code = '%s', title = '%s', department = '%s'), description = '%s'>" % (
			self.course_code, self.title, self.department, self.description)

def start():
	Base.metadata.create_all(engine)
	
	session.commit()

def read_schedule():
	engi_data = pd.read_csv(ENGI_SCHEDULE_FILE)
	print engi_data

def main():
	# start()
	read_schedule()

main()
	
	