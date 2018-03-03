from gensim.models import doc2vec
from gensim import matutils
from numpy import array
import pandas as pd
import logging


def predict_course(model, query_list, n=10):
	"""
	Given a pretrianed model and a list of query words, return the top-n related course with cosine similarity.
	If the keyword is not in the key set, return None.
	:param n: get top-n related course; default n = 5
	:param model: a doc2vec model
	:param query_list: a list of query word
	:type model: doc2vec.Doc2Vec
	:type query_list: str
	:return: [(tag, cosine_similarity)]
	"""
	dv = model.docvecs
	
	def get_vector(model, query_list):
		"""
		Return the sum vector of a list of words
		:type model: doc2vec.Doc2Vec
		:type query_list: list
		"""
		strlist = query_list.split(" ")
		v = [model[i] for i in strlist]
		return matutils.unitvec(array(v).mean(axis=0))
	
	try:
		sum_vec = get_vector(model, query_list)
	except KeyError as e:
		print 'Can\'t find key.'
		print e
		return None
	result = model.docvecs.most_similar([sum_vec], topn=n)
	course_code_result = []
	subject_code_result = []
	for i in result:
		if (len(i[0]) == 4):
			subject_code_result.append(i)
		else:
			course_code_result.append(i)
	
	# sort subject_code
	subject_code_result.sort(key=lambda x: x[1])
	
	# weights course
	for subject in subject_code_result:
		temp_course = []
		for course in course_code_result:
			# print course[0][:4]
			if course[:4] == subject:
				temp_course.append(course)
			# print temp_course
	
	return course_code_result


# return subject_code_result, course_code_result
#
# def read_data():
# 	with open('data/catalog.xlsx', 'r') as f:
# 		catalog = pd.read_excel(f)  # type: pandas.core.frame.DataFrame
# 	return catalog


def predict(query_string):
	"""
	
	:param query_string:
	:type query_string: str
	:return:
	"""
	
	model = doc2vec.Doc2Vec.load('trainedmodel/epoch100_pretrained_singletag')
	predict = predict_course(model, query_string)
	
	return predict
