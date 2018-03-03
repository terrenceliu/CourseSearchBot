from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from makedb import Course
import sqlalchemy


"""
	Configuration
"""
engine = create_engine('postgresql://localhost/course_catalog')
# start session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def get_course_by_code(input):
	"""
	
	:param input: the input string
	:type input: str
	:return:
	"""
	# query singleton
	q = session.query(Course) # type: sqlalchemy.orm.query.Query
	print q.filter_by(course_code='COMP182').first()

def test():
	get_course_by_code('COMP182')

test()
