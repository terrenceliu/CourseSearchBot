from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

CATALOG_FILE = 'data/catalog.xlsx'

"""
	Configuration
"""
Base = declarative_base()
engine = create_engine('postgresql://localhost/catalog')
# start session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

"""
	Model
"""
class Course(Base):
	__tablename__ = 'course'
	id = Column(Integer, primary_key=True)
	course_code = Column(String)
	title = Column(String)
	department = Column(String)
	long_title = Column(String)
	description = Column(String)
	distribution = Column(String)
	prerequisites = Column(String)
	course_type = Column(String)
	grade_mode = Column(String)
	credit_hours = Column(String)

	def __repr__(self):
		"""
		Define the representation of the database.
		:return:
		"""
		return "<Course(courde code = '%s', title = '%s', department = '%s'), description = '%s'>" % (
			self.course_code, self.title, self.department, self.description)



def read_excel(f):
	"""
	
	:param f: excel file of course catalog
	:type f: file
	:return df: the dataframe of parsed excel file
	"""
	
	catalog = pd.read_excel(f, na_values='null', keep_default_na = False).fillna("")  # type: pandas.core.frame.DataFrame
	
	return catalog


def add_catalog_to_db(session, catalog):
	"""
	Add course catalog to the database
	:param session: Session
	:param catalog: course catalog dataframe
	:type session: sqlalchemy.orm.session.Session
	:type catalog: pandas.core.frame.DataFrame
	:return:
	"""
	
	course_code = ""
	title = ""
	department = ""
	long_title = ""
	description = ""
	credit_hours = ""
	distribution_group = ""
	prerequisites = ""
	course_type = ""
	grade_mode = ""
	
	course_list = []
	
	# Create course instances
	for id, row in catalog.iterrows():
		# Read value
		for index, value in row.iteritems():
			if (index == u"course_code"):
				course_code = value
			elif (index == u"title"):
				title = value
			elif (index == u"department"):
				department = value
			elif (index == u"long_title"):
				long_title = value
			elif (index == u"description"):
				description = value
			elif (index == u"credit_hours"):
				credit_hours = value
			elif (index == u"distribution_group"):
				distribution_group = value
			elif (index == u"prerequisites"):
				prerequisites = value
			elif (index == u"course_type"):
				course_type = value
			elif (index == u"grade_mode"):
				grade_mode = value
			else:
				print index, value
				continue
		
		
		# Crease course instance
		course = Course(course_code=course_code, title=title,
		                department=department, long_title=long_title, description=description,
		                credit_hours = credit_hours, distribution = distribution_group, prerequisites = prerequisites,
		                course_type = course_type, grade_mode = grade_mode)
		course_list.append(course)
	
	# Add course instances into the database
	for course in course_list:
		session.add(course)

def test():
	print session.query(Course).first()
	
def start():
	# create table
	Base.metadata.create_all(engine)
	
	# read excel
	catalog = read_excel(CATALOG_FILE)
	
	# add course to db
	add_catalog_to_db(session, catalog)
	
	session.commit()
	

def main():
	start()
	# test()
	
# main()