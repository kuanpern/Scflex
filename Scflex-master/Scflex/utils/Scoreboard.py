import os
from numpy import *
from copy import deepcopy
import pandas as pd

class Scoreboard:
	def __init__(self, name = None, specifications = {}, specification_files = []):
		self.portfolio_data = pd.DataFrame()
		self.name = name

		# working memory
		self.display_history_processes = []
		self.temp_files = []

		# read specifications
		self.specifications = specifications
		for specification_file in specification_files:
			self.specifications.update(read_specification_file(specification_file))
		# end for

		# initialize format setter
		self.initialize_xlsx_format_setter()
	# end def

	def __len__(self):
		return len(self.portfolio_data)
	# end def

	def __repr__(self):
		txt = 'Score board with '+str(len(self.portfolio_data))+' entries'
		if self.name != None:
			txt = txt + ' in ' + self.name
		# end if
		return txt
	# end def

	def initialize_xlsx_format_setter(self):
		def xlsx_cell_bgcolor_setter(det):
			det = str(det).upper()
			try:
				color = bg_color_dict[det]
			except KeyError:
				color = 'white' # <- default color
			# end try

			return {'bg_color': color}
		# end def

		if 'bg_color_dict' in self.specifications:
			bg_color_dict = self.specifications['bg_color_dict']
		else:
			bg_color_dict = {}
		# end if

		self.xlsx_format_setter = xlsx_cell_bgcolor_setter(bg_color_dict)
	# end def

	def read_portfolio(self, filename, index_name = None, sep='\t', infer_datetime_format=True, na_values = ['--', None], converters = {}):

		# read portfolio
		contents = pd.read_csv(filename, sep='\t', infer_datetime_format=infer_datetime_format, na_values = na_values, converters=converters, index_col=False)
		if index_name == None: index_name = contents.columns[0]
		self.portfolio_data = pd.DataFrame(contents).set_index(index_name)
	# end def

	def keys(self):
		return self.portfolio_data.index
	# end def

	def data(self, key):
		return self.portfolio_data.ix[key]
	# end def

	def features(self):
		return self.portfolio_data.keys()
	# end def

	def join_boards(self, boards):
		assert set([self.portfolio_data.index.name]) == set([board.index.name for board in boards])
		for board in boards:
			self.portfolio_data = self.portfolio_data.combine_first(board)
		# end for
	# end def

	def each_append_scorer(self, scorer):
		self.portfolio_data = scorer(self.portfolio_data)
	# end def

	def across_comparer(self, rater, scorer_name, new_score_name):
		s = deepcopy(self.portfolio_data[scorer_name])
		index, values = [s.index, s.values]
		ratings = rater(values)		
		self.portfolio_data[new_score_name] = pd.Series(ratings, index = index)
	# end def

	def pop_entries(self, scorer_name, filter_function, inplace = False):
		# filter_function is negative selector. True -> pop
		dets = map(filter_function, self.portfolio_data[scorer_name])
		contents = self.portfolio_data[scorer_name][dets]
		if inplace == True:
			self.portfolio_data = contents
		else:
			return deepcopy(self)
		# end if
	# end def

	def retain_entries(self, scorer_name, filter_function, inplace = False):
		# filter_function is positive selector. False -> pop_
		return self.pop_entries(scorer_name, lambda x: not(filter_function(x)), inplace)
	# end def

	def remove_feature(self, feature_name):
		self.portfolio_data.pop(feature_name)
	# end def

	def retrieve_feature(self, feature_name):
		return dict(self.portfolio_data[feature_name])
	# end def

	def write_to_files(self, root, sep='\t', sort_keys = None):
		# determine filenames
		tsv_filename, xlsx_filename = [root + '.tsv', root + '.xlsx']

		# make and sort the table
		out_data = self.portfolio_data.sort(sort_keys)

		# print tsv output
		self.portfolio_data.to_csv(tsv_filename, sep=sep)

		# convert to xlsx output
		tsv2xlsx(xlsx_filename, [tsv_filename], self.xlsx_format_setter)

		return tsv_filename, xlsx_filename
	# end def
		

	def display_board(self, spreadsheet_engine = 'gnumeric', refresh = True, sort_keys = None):
		# write to temporary file
		root = unique_name() + '.tmp'
		tsv_filename, xlsx_filename = self.write_to_files(root, sep='\t', sort_keys = sort_keys)
		self.temp_files.extend([tsv_filename, xlsx_filename])
		
		# use spreadsheet engine to open the xlsx file
		cmd = spreadsheet_engine + ' ' + xlsx_filename
		process = subprocess.Popen(cmd.split())
		if refresh == True:
			for old_process in self.display_history_processes:
				old_process.terminate()
			# end for
		# end if
		self.display_history_processes.append(process)
	# end def

	def clear_temporary_files(self):
		for fname in self.temp_files:
			os.remove(fname)
		# end for
		self.temp_files = []
	# end def

# end class

'''
class Scorer: # i.e. rule
	def __init__(self, rule_filename = None):
		if rule_filename != None:
			self.read_rule(rule_filename)
		# end if
		self.initialize()
	# end def

	def read_rule(self, rule_filename):
		self.rule_filename = rule_filename
	# end def

	def initialize(self):
		# read rule name and description
		lines = open(self.rule_filename).readlines()
		lines = [line.strip() for line in lines if line.strip().startswith('#')]
		self.name, self.description = ['', '']
		for line in lines:
			if line.startswith('# Name:'):
				self.name        = line.replace('# Name:', '')       .strip()
			if line.startswith('# Description:'):
				self.description = line.replace('# Description:', '').strip()
		# end for
	# end def

	def __repr__(self):
		return self.name + ' ' + self.description
	# end def
# end class
'''

# ------ BELOW ARE GENERIC OPERATOR FUNCTIONS ------ #
def is_in(s):
	f = lambda x: x in s
	return f
# end def

def not_in(s):
	f = lambda x: x not in s
	return f
# end def

def less_than(cutoff):
	f = lambda x: x <= cutoff
	return f
# end def

def greater_than(cutoff):
	f = lambda x: x >= cutoff
	return f
# end def

def within(lb, ub):
	lb, ub = sorted([lb, ub])
	f = lambda x: lb <= x and x <= ub
	return f
# end def

def outside(lb, ub):
	lb, ub = sorted([lb, ub])
	f = lambda x: lb > x or x < ub
	return f
# end def

def equals(target):
	f = lambda x: x == target
	return f
# end def

def not_equals(target):
	f = lambda x: x != target
	return f
# end def

def is_missing(na_list = [None, '--']):
	f = lambda x: x in na_list or isnan(x)
	return f
# end def

'''
def rank_comparer_generator(arrange = 'ascending', percentile_normalize = False):
	def f(S):
		sorter = zip(S, range(len(S)))
		sorter.sort()
		if arrange == 'descending':
			sorter.reverse()
		# end if
		x, y = zip(*sorter)
		output = [None for i in range(len(S))]
		for i in range(len(y)):
			output[y[i]] = i
		# end for

		if percentile_normalize == True:
			output = [out / float(len(S)) * 100 for out in output]
		# end if

		return output		
	# end def
	return f
# end def

def generic_scorer_generator(features, fx, target_name = 'SCORE'):
	def f(stock_obj):
		values = [stock_obj.data[feature] for feature in features]
		output = fx(values)
		output = output.flatten().tolist()[0]
		stock_obj.data[target_name] = output
	# end def
	return f
# end def

def slr_generator(features, coefs, target_name = 'SCORE'):
	def f(stock_obj):
		values = [stock_obj.data[feature] for feature in features]
		output = dot(coefs[:-1], values) + coefs[-1]
		stock_obj.data[target_name] = output
	# end def
	return f
# end def

def assign_value_generator(feature_name, value):
	def f(stock_obj):
		stock_obj.data[feature_name] = value
	# end def
	return f
# end def
'''




