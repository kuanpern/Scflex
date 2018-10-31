#!/usr/bin/python
# functions to manage (add, remove) Scflex task
import uuid
import datetime
import common_utils as utils
import logging
import getpass
import time
logger = logging.getLogger()
from shorthand import require_inputs

class Scflex_controller:
	database_name   = None
	collection_name = None
	default_engine_conf = {
	  'batch_size'         : 8,
	  'max_timeout'        : 600,
	  'refresh_interval'   : 60,
	  'hibernation_period' : 10,
	  'max_failure_n'      : 5,
	  'min_repeat_interval': 0,
<<<<<<< HEAD
=======
	  'uuid'               : str(uuid.uuid4())
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
	}

	# ========================== INTEGRITY CHECKS ========================== #
	@staticmethod
	@require_inputs(['executable', 'cmd_args', 'working_dir', 'timeout'])
	def check_program_pars(program_pars):
		return {'status': True}
	# end if

	@staticmethod
	@require_inputs(['name', 'batch_size', 'max_timeout', 'refresh_interval', 'hibernation_period', 'max_failure_n', 'min_repeat_interval'])
	def check_engine_pars(engine_conf):
		return {'status': True}
	# end if
	# ====================== END INTEGRITY CHECKS ========================== #

	def __init__(self, db_pars):
		logger.info('Scflex controller initialized')
		self.db_pars = db_pars
	# end def

	def set_task_list(self, database_name, collection_name):
		logger.info('task list set as "%s"' % (str(database_name)+':'+str(collection_name)))
		self.database_name   = database_name
		self.collection_name = collection_name
	# end def

	def init_task_list(self, database_name, collection_name, engine_conf):
		db, db_client = utils.connect_mongoDB_server(self.db_pars)

<<<<<<< HEAD
=======
		"""
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
		det_existed = False
		if database_name in db_client.database_names():
			if collection_name in db_client[database_name].collection_names():
				logger.warning('task list already exists. To modify engine, please use Scflex_controller.update_congine_conf() method .')
				return
			# end if
		# end if
<<<<<<< HEAD
=======
		"""
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5

		# 1. insert engine conf into collection
		res = self.check_engine_pars(engine_conf)
		if not(res['status']):
			logging.error(str(res['errors']))
			return
		# end if

		engine_conf.update({
		  'role'          : 'engine_conf',
		  'task_db_name'  : database_name,
		  'task_coll_name': collection_name,
		  'uuid'          : str(uuid.uuid4()),
		  'date_created'  : datetime.datetime.utcnow().isoformat(),
		  'created_by'    : getpass.getuser()
		})
		# insert to database
		res_create = db_client[database_name][collection_name].insert_one(engine_conf)
		# set indexes
		db_client[database_name][collection_name].create_index('_id')
		db_client[database_name][collection_name].create_index('role')

		# 2. register to Scflex_control
		res_register = db_client['Scflex_control']['task_list_monitoring'].insert_one({
			"role"         : "task_list_info",
			"db_name"      : database_name,
			"coll_name"    : collection_name,
			"creation_time": time.time(),
			"uuid"         : str(uuid.uuid4())
		}) # end insert

		# close connection
		db_client.close()

		# set self's task list
		self.set_task_list(database_name, collection_name)

		output = {
		  'create'  : {_: getattr(res_create,   _) for _ in dir(res_create)   if not(_.startswith('_'))},
		  'register': {_: getattr(res_register, _) for _ in dir(res_register) if not(_.startswith('_'))}
		}

		return output
	# end def

	# ========================== MONITORING RELATED ========================== #
	def update_engine_conf(self, engine_conf):
		if self.database_name == None or self.collection_name == None:
			logging.error('task list not selected.')
			return
		# end if

		res = self.check_engine_pars(engine_conf)
		if not(res['status']):
			logging.error(str(res['errors']))
			return
		# end if

		# update the database 
		db, db_client = utils.connect_mongoDB_server(self.db_pars)
		coll = db_client[self.database_name][self.collection_name]
		res = coll.update_one(
		  {'role': 'engine_conf'},
<<<<<<< HEAD
		  {'set' :  engine_conf }
=======
		  {'$set':  engine_conf },
		  upsert=True
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
		) # end update one
		return res
	# end def

	def display_task_statuses(self, skip=0, limit=0):
		db, db_client = utils.connect_mongoDB_server(self.db_pars)
		cursor = db_client[self.database_name][self.collection_name].find(
			{'role': 'task'}, {'name': True, 'status': True}
		).skip(skip).limit(lmit)
		records = list(cursor)
		db_client.close()

		# formatting a little
		output = []
		for rec in records:
			status = rec.pop('status')
			rec.update(status)
			output.append(rec)
		# end for

		return output
	# end def

	def display_engine_pars(self):
		db, db_client = utils.connect_mongoDB_server(self.db_pars)
		ans = db_client[self.database_name][self.collection_name].find_one(
			{'role': 'engine_conf'}
		) # end cursor
		db_client.close()

		return ans
	# end def

	# ====================== END MONITORING RELATED ========================== #


<<<<<<< HEAD
	# ========================== TASK RELATED ========================== #
	def add_task(self, name, executable, cmd_args, working_dir, timeout = 300):
=======

	# ========================== TASK RELATED ========================== #
	def add_task(self, name, executable, cmd_args, working_dir, min_repeat_interval=0, timeout = 300):
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
		program_pars =  {
			'timeout'    : timeout,
			'executable' : executable,
			'cmd_args'   : cmd_args,
<<<<<<< HEAD
			'working_dir': working_dir
=======
			'working_dir': working_dir,
			'min_repeat_interval': min_repeat_interval,
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
		} # end pars

		return self.add_task_program(name=name, program_pars=program_pars, timeout=timeout)
	# end def

	def add_task_by_dict(self, input_pars):
		return self.add_task(**input_pars)
	# end def
<<<<<<< HEAD
=======

	def check_program_pars(self, program_pars):
		requireds = ["program_type", "working_dir", "exe_path", "exe_flags", "exe_args"]
		missings = list(set(requireds) - set(program_pars.keys()))
		assert len(missings) == 0, 'missing paramters ' + str(missings)

		if "template" in program_pars["program_type"]:
			requireds = ["db_pars_path", "conf_loc"]
			missings = list(set(requireds) - set(program_pars.keys()))
			assert len(missings) == 0, 'missing paramters ' + str(missings)
		# end if
	# end if
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5

	def deactivate_task_program(self, name):
		db, db_client = utils.connect_mongoDB_server(self.db_pars)
		response = db_client[self.database_name][self.collection_name].update_one(
		  {'role': 'task', 'name': name},
		  {'$set': {'status.status': 'inactive'}}
		) # end update
		return response
	# end def

	def delete_task_program(self, name):
		db, db_client = utils.connect_mongoDB_server(self.db_pars)
		response = db_client[self.database_name][self.collection_name].delete_one(
		  {'role': 'task', 'name': name},
		) # end update
		return response
	# end def

	def add_task_program(self, name, program_pars, uuid_label = None, timeout = 300):
		# 1. data integrity check
		res = self.check_program_pars(program_pars)
		if not(res['status']):
			logging.error(str(res['errors']))
			return
		# end if

		# connect to collection
		db, db_client = utils.connect_mongoDB_server(self.db_pars)

		# name must be unique within the task-list
		logger.info('checking task list')
		_ = db_client[self.database_name][self.collection_name].find_one({'name': name})
		if _ != None:
			msg = 'task "%s" already exists.' % (name)
			return {'status': 'failed', 'errors': [msg]}
		# end if

		# make uuid label if it's not provided
		if uuid_label == None:
			uuid_label = str(uuid.uuid4())
		# end if

		# make document
		_task = {
		  'name'        : name,
		  'role'        : 'task',
		  'uuid'        : uuid_label,
		  'date_created': datetime.datetime.utcnow().isoformat(),
		  'historicals' : [],
		  'status': {
		    'status'       : 'active',
			'last_updated' : 0,
			'last_success' : 0,
			'last_failure' : 0,
			'failure_n'    : 0,
			'priority_r'   : 1.0,
			'last_response': {
			  'status_code': -1,
			  'info': {
			    'duration': -1
			  }
			}
		  },
		  'program_pars': program_pars
		} # end _task

		# insert doc
		logger.info('inserting new task')
		res = db_client[self.database_name][self.collection_name].insert(_task)
		return res
	# end def
	# ===================== END TASK RELATED ========================== #

# end class
<<<<<<< HEAD


# interface example
"""
>> controller = Scflex_controller(db_pars)	
>> engine_conf = controller.default_engine_conf
>> engine_conf['name'] = 'task-list-name'
>> controller.init_task_list(db_name, coll_name, engine_conf)
>> controller.set_task_list(db_name, coll_name)
>> controller.add_task_by_dict({
  'name'       : 'test-task',
  'timeout'    : 300,
  'executable' : '/bin/ls',
  'cmd_args'   : [{'all': ''}],
  'working_dir': '/home/kuanpern/'
})
"""



=======


# interface example
"""
>> controller = Scflex_controller(db_pars)	
>> engine_conf = controller.default_engine_conf
>> engine_conf['name'] = 'task-list-name'
>> controller.init_task_list(db_name, coll_name, engine_conf)
>> controller.set_task_list(db_name, coll_name)
>> controller.add_task_by_dict({
  'name'       : 'test-task',
  'timeout'    : 300,
  'executable' : '/bin/ls',
  'cmd_args'   : [{'all': ''}],
  'working_dir': '/home/kuanpern/'
})
"""
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
