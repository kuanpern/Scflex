#!/usr/bin/python

from shorthand import *
import Scflex
import Scflex.utils
import Scflex.conf
import uuid
import yaml

class Controller:
	def __init__(self, pars):
		self.db_pars = pars
		self.connect_db()
		self.cur_portfolio = None
	# end def

	def connect_db(self):
		self.db, self.client = Scflex.utils.connect_mongoDB_server(self.db_pars)
	# end def

	def current_portfolio(self):
		return self.cur_portfolio
	# end def

	def list_portfolio(self):
		return self.db.collection_names()
	# end def

	def use_portfolio(self, portfolio_name):
		assert portfolio_name in db.collection_names(), '%s not in database.' % portfolio_name
		self.cur_portfolio = portfolio_name
	# end def

	def create_portfolio(self, portfolio_name, log_filename_root, batch_size = 100, log_rotate_freq = 'day'):
		assert portfolio_name not in db.collection_names(), '%s already in database.' % portfolio_name
		# input validity checking ..
		batch_size = int(batch_size)
		avails = ['min', 'hour', 'day', 'week', 'month']
		assert log_rotate_freq in avails, '"log_rotate_freq" can only be within '+str(avails)

		# insert to MongoDB
		content = {
			'_uuid': str(uuid.uuid4()),
			'name': name,
			'role': 'engine',
			'log_filename_root': log_filename_root,
			'batch_size': batch_size,
			'log_rotate_freq': log_rotate_freq
		} # end content
		self.db[portfolio_name].insert(content)
	# end def

	def drop_portfolio(self, portfolio_name):
		assert portfolio_name in db.collection_names(), '%s not in database.' % portfolio_name
		self.db.drop_collection(portfolio_name)
		if self.cur_portfolio == portfolio_name:
			self.cur_portfolio = None
		# end if
	# end def

	def update_portfolio_pars(self, pars):
		assert type(pars) == dict
		# retrieve
		obj = self.db[portfolio_name].find_one({'role': 'engine'})
		# remove
		self.db[portfolio_name].remove({'role': 'engine'})
		# update
		obj.update(pars)
		obj['_uuid'] = str(uuid.uuid4())
		obj['role'] = 'engine'
		# insert back
		self.db[portfolio_name].insert(obj)
	# end def


	@required('cur_portfolio')
	def describe_portfolio(self, pretty_print = False, print_only = True):
		obj = self.db[self.cur_portfolio].find_one({'role': 'engine'})
		if pretty_print:
			# to-do: prettily print result
			if print_only:
				return
			# end if
		# end if
		return obj
	# end def

	@required('cur_portfolio')
	def list_tasks(self, pretty_print = False, print_only = True):
		obj = list(self.db[self.cur_portfolio].find({'role': 'task'}))
		if pretty_print:
			# to-do: prettily print result
			if print_only:
				return
			# end if
		# end if
		return obj
	# end def

	@required('cur_portfolio')
	def insert_task(self, name, exectype, exe, log_filename):
		# input validity checking ..
		avails = ['registered', 'executable', 'binary', 'url']
		assert exectype in avails, '"exectype" can only be within '+str(avails)

		# insert to MongoDB
		_id = str(uuid.uuid4())
		ts = utc_timestamp()
		content = {
			'_uuid': _id,
			'name': name,
			'role': 'task',
			'exectype': exectype,
			'exec': exe,
			'log_filename': log_filename,
			'time_created': ts,
			'last_accessed': 0
		} # end content

		self.db[self.cur_portfolio].insert_one(content)
		return _id
	# end def

	@required('cur_portfolio')
	def remove_task(self, task_id):
		self.db[self.cur_portfolio].remove({'_uuid': task_id})
	# end def

	@required('cur_portfolio')
	def describe_task(self, task_id):
		obj = list(self.db[self.cur_portfolio].find({'_uuid': task_id}))
		if pretty_print:
			# to-do: prettily print result
			if print_only:
				return
			# end if
		# end if
		return obj
	# end def

	def quit(self):
		self.client.close()
	# end def
# end class


# some tests ...
import sys
if len(sys.argv) != 2:
	print sys.argv[0], 'input.json'
	sys.exit(0)
# end if

pars = yaml.load(open(Scflex.conf.conf_path + 'Scflex.yaml'))
db_pars = pars['database']['mongodb']

controller = Controller(db_pars)

