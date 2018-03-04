import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import predict
from makedb import Course
from make_schedule import Schedule

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
	
	def format_course_output(self, course, schedule):
		"""
		Format the output of a course
		:param course:
		:type course: Course
		:param schedule:
		:type schedule: Schedule
		:return:
		:rtype: str
		"""
		
		# handle schedule
		str_list = schedule.schedule.strip().split(' ')
		sch_res = ''
		if (len(str_list) >= 6):
			val_list = str_list[:6]
			val_list[5] = val_list[5][:3]
			
			# time
			time = val_list[0] + ' ' + val_list[1] + ' ' + val_list[2] + ' ' + val_list[3]
			location = val_list[4] + ' ' + val_list[5]
			sch_res = str(time + '\t' + location)
		
		res = ""
		res += 'Course code: ' + course.course_code + '\n'
		res += 'Title: ' + course.title + '\n'
		res += 'Department: ' + course.department + '\n'
		res += 'Credit Hours: ' + course.credit_hours + '\n'
		res += 'Description: ' + course.description + '\n'
		if (sch_res != ''):
			res += 'Schedule: ' + sch_res + '\n'
		res += 'Instructor: ' + schedule.instructor + '\n'
		return res

"""
	Configuration
"""
catalog_engine = create_engine('postgresql://localhost/catalog')
# schedule_engine = create_engine('postgresql://localhost/schedule')

# start session
Session_cat = sessionmaker()
Session_cat.configure(bind=catalog_engine)
session_cat = Session_cat()

# Session_sch = sessionmaker()
# Session_sch.configure(bind=schedule_engine)
# session_sch = Session_sch()

"""
	Singleton
"""
# query singleton
query_cat = session_cat.query(Course) # type: sqlalchemy.orm.query.Query

query_sch = session_cat.query(Schedule)

# util singleton
util = Util()

# null object of Course
null_course = Course(course_code = 'Null', title = 'Null')


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
	
	course = query_cat.filter(Course.course_code == input).first()
	schedule = query_sch.filter(Schedule.course_code == input).first()
	
	if (course != None and schedule != None):
		res = util.format_course_output(course, schedule)
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
	
	if search_result == None:
		return "Can't locate any class with keyword \'" + user_input + "\'. Try another key word?"
	
	course_list = []        # [(course: Course, similarity: double)]
	for res in search_result:
		course_code = res[0]
		prob = res[1]
		course = query_cat.filter(Course.course_code == course_code).first()
		schedule = query_sch.filter(Schedule.course_code == course_code).first()
		
		if course == None or schedule == None:
			continue
		else:
			course_list.append((course, schedule, prob))
	
	res = ""
		
	for ele in course_list:
		res += "Probability = " + str(float(format(ele[2], '.3f'))) + "\n"
		res += util.format_course_output(ele[0], ele[1])
		res += "\n"
		
	return res