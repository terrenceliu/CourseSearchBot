from sqlalchemy import Integer, Column, create_engine, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload, subqueryload, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np

# CATALOG_FILE = 'data/engineering_schedule.csv'
ENGI_FILE = './data/engi.csv'
HUMA_FILE = './data/human.csv'
SOCI_FILE = './data/social.csv'
NATR_FILE = './data/natural.csv'
DEAN_FILE = './data/dean.csv'

"""
	Configuration
"""
Base = declarative_base()
engine = create_engine('postgresql://localhost/catalog')

# start session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Schedule(Base):
	__tablename__ = 'schedule'
	id = Column(Integer, primary_key=True)
	crn = Column(String)
	course_code = Column(String)
	session = Column(String)
	title = Column(String)
	instructor = Column(String)
	schedule = Column(String)
	credit = Column(String)
	
	
	def __repr__(self):
		"""
		Define the representation of the database.
		:return:
		"""
		return "<Course(courde code = '%s', title = '%s', department = '%s'), description = '%s'>" % (
			self.course_code, self.title, self.department, self.description)

def read_schedule():
	"""
	
	:return: dataframe
	:rtype: pandas.core.frame.DataFrame
	"""
	engi_data = pd.read_csv(ENGI_FILE, sep=';', na_values='')  # type: pandas.core.frame.DataFrame
	huma_data = pd.read_csv(HUMA_FILE, sep = ';', na_values='') # type: pandas.core.frame.DataFrame
	soci_data = pd.read_csv(SOCI_FILE, sep = ';', na_values='') # type: pandas.core.frame.DataFrame
	natr_data = pd.read_csv(NATR_FILE, sep = ';', na_values='') # type: pandas.core.frame.DataFrame
	dean_data = pd.read_csv(DEAN_FILE, sep = ';', na_values='') # type: pandas.core.frame.DataFrame
	
	aggregate_data = [engi_data, huma_data, soci_data, natr_data, dean_data]
	
	# concat
	total_df = pd.concat(aggregate_data)
	
	# fill in na
	total_df.fillna('', inplace=True)
	
	return total_df


def add_catalog_to_db(db_session, catalog):
	"""
	Add course catalog to the database
	:param session: Session
	:param catalog: course catalog dataframe
	:type session: sqlalchemy.orm.session.Session
	:type catalog: pandas.core.frame.DataFrame
	:return:
	"""
	crn = ""
	course_code = ""
	session = ""
	title = ""
	instructor = ""
	schedule = ""
	credit = ""
	
	"""
		CRN;
		Course;
		Session;
		Title;
		Instructor;
		Time/Location;
		Credits
	"""
	
	schedule_list = []
	
	# Create course instances
	for id, row in catalog.iterrows():
		# Read value
		for index, value in row.iteritems():
			if index == 'CRN':
				crn = value
			elif index == 'Course':
				str_list = value.strip().split(' ')
				if (len(str_list) != 3):
					# print str_list
					continue
				else:
					res = ""
					for i in range(len(str_list) - 1):
						res += str_list[i]
					# print res
				course_code = res
				# course_code = value
				
			elif index == 'Session':
				session = value
			elif index == 'Title':
				title = value
			elif index == 'Instructor':
				instructor = value
			elif index == 'Time/Location':
				# str_list = value.strip().split(' ')
				# if (len(str_list) < 6):
				# 	continue
				# else:
				# 	val_list = str_list[:6]
				# 	val_list[5] = val_list[5][:3]
				#
				# 	# time
				# 	time = val_list[0] + ' ' + val_list[1] + ' ' + val_list[2] + ' ' + val_list[3]
				# 	location = val_list[4] + ' ' + val_list[5]
				# schedule = str(time + '\t' + location)
				schedule = value
			elif index == 'Credits':
				credit = value
			else:
				print index, value
				continue
			
		# Create new scheudle instance
		schedule = Schedule(crn = crn, course_code = course_code, session = session, title = title,
		                    instructor = instructor, schedule = schedule, credit = credit)
		
		# add instance into list
		schedule_list.append(schedule)
		
	# Add schedule into database
	for ele in schedule_list:
		db_session.add(ele)


def start():
	Base.metadata.create_all(engine)
	
	# read excel
	catalog = read_schedule()

	# add catalog into db
	add_catalog_to_db(session, catalog)
	
	session.commit()
	
def main():
	start()

main()