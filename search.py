from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from makedb import Course

"""
	Class
"""

class Util():
	def strip_whitespace(self, text):
		"""
		Strip the front and rear whitespace of a given text
		:param text: the given string
		:type text: str
		:return:
		:rtype: str
		"""
		return text.strip()

"""
	Configuration
"""
engine = create_engine('postgresql://localhost/course_catalog')

# start session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

"""
	Singleton
"""
# query singleton
query = session.query(Course) # type: sqlalchemy.orm.query.Query

# util singleton
util = Util()

# null object of Course
null_course = Course(course_code = 'Null', title = 'Null', )

def get_course_by_code(input):
	"""
	Given the input string (course code), return the course
	:param input: the input course code
	:type input: str
	:return: a course instance
	:rtype: Course
	"""
	
	res = None
	res = query.filter(Course.course_code == input).first()
	# print res
	
	
def test():
	# course = get_course_by_code('COMP121')
	print util.strip_whitespace(" hello world  ")
	

test()
