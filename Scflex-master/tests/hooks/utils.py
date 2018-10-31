from Scflex.utils.task_management_utils import Scflex_controller
import yaml

db_pars_path = '/home/scube_backend/Scube_root/Scube-master/Scube/services/financials_update/scflex_hook/setups/.keys/mongo_pars.yaml'
db_pars = yaml.load(open(db_pars_path))

class scflex_task_manager():
	task_list_name  = None
	database_name   = None
	collection_name = None

	def __init__(self, db_pars):
		self.db_pars = db_pars
		self.controller = Scflex_controller(self.db_pars)
		self.controller.set_task_list(self.database_name, self.collection_name)
	# end def

	def initialize_task_list(self, max_failure_n = 5, max_timeout = 600, refresh_interval = 600, hibernation_period = 0, batch_size = 20,  min_repeat_interval = 0):
		'''warning: run only once'''
		print 'initializing task list:', self.task_list_name, '@', self.database_name+':'+self.collection_name
		ans = self.controller.add_task_list(
			task_list_name      = self.task_list_name,
			database_name       = self.database_name,
			collection_name     = self.collection_name,
			max_failure_n       = max_failure_n,
			max_timeout         = max_timeout, 
			refresh_interval    = refresh_interval, 
			hibernation_period  = hibernation_period,
			batch_size          = batch_size,
			min_repeat_interval = min_repeat_interval
		) # end adding task list

		return ans
	# end def

	def add_task_template_from_file(self, conf_path):
		conf_doc = yaml.load(open(conf_path))
		return self.controller.add_task_template(conf_doc)
	# end def

	def add_task(self, name, program_pars, timeout):
		return self.controller.add_task_program(name=name, program_pars=program_pars, timeout=timeout)
	# end def

	def deactivate_task(self, name):
		return self.controller.deactivate_task_program(name=name)
	# end def

# end class

