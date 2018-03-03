from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from makedb import Course
import predict

"""
	Class
"""

class Util():
	def strip_whitespace(self, text):
		"""
		Strip the leading and trailing whitespace of a given text
		:param text: the given string
		:type text: str
		:return:
		:rtype: str
		"""
		return text.strip()
	
	def del_whitespace(selfs, text):
		"""
		Delete any whitespace in a given string
		:param text:
		:type text: str
		:return:
		:rtype: str
		"""
		return text.replace(' ', '')
	
	def to_upper(self, text):
		"""
		Uppercase all characer in a given string
		:param text:
		:type text: str
		:return:
		:rtype: str
		"""
		return text.upper()
	
	def format_course_output(self, course):
		"""
		Format the output of a course
		:param course:
		:type course: Course
		:return:
		:rtype: str
		"""
		res = ""
		res += 'Course code: ' + course.course_code + '\n'
		res += 'Title: ' + course.title + '\n'
		res += 'Department: ' + course.department + '\n'
		res += 'Credit Hours: ' + course.credit_hours + '\n'
		res += 'Description: ' + course.description + '\n'
		return res

"""
	Configuration
"""
engine = create_engine('postgresql://localhost/catalog')

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


"""
	Method
"""
def get_course_by_code(input):
	"""
	Given the input string (course code), return the course
	:param input: the input course code
	:type input: str
	:return: a string representation of a course instance
	:rtype: str
	"""
	res = None
	user_input = input
	input = str(input)
	# clean input
	input = util.strip_whitespace(input)
	input = util.del_whitespace(input)
	input = util.to_upper(input)
	
	print input
	
	course = query.filter(Course.course_code == input).first()
	
	if (course != None):
		res = util.format_course_output(course)
	else:
		res = "Sry seems like I can't find " + user_input
	return res
	
def get_course_by_key_words(input):
	"""
	Given the input string (key words), return the course
	:param input: the input course code
	:type input: str
	:return: a course instance
	:rtype: Course
	"""

def get_course_by_predict(input):
	"""
	:param input:
	:return:
	"""
	user_input = input
	input = str(input)
	# clean input
	
	input = util.strip_whitespace(input)
	
	print "input = " + input
	
	search_result = predict.predict(input)      # [(course_code: str, similarity: double)]
	
	course_list = []        # [(course: Course, similarity: double)]
	for res in search_result:
		course_code = res[0]
		prob = res[1]
		course = query.filter(Course.course_code == course_code).first()

		if course == None:
			continue
		else:
			course_list.append((course, prob))
	
	res = ""
		
	for ele in course_list:
		res += "Similarity = " + str(ele[1]) + "\n"
		res += util.format_course_output(ele[0])
		res += "\n"
		
	return res