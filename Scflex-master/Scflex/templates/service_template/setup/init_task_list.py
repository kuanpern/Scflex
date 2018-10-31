#!/usr/bin/python
import sys
import yaml
import common_utils as utils
from Scflex.utils.task_management_utils import Scflex_controller
import logging
logging.basicConfig()

if __name__ == '__main__':
	print 'Please examine the file and preferrably run interactively.'
	sys.exit(0)
# end if

# read mongodb credential file
mongo_cred_file = '{{ mongodb_credential_file }}'
db_pars = yaml.load(open(mongo_cred_file))

# initiate the controller
controller = Scflex_controller(db_pars)
# load default engine parameter
engine_conf = controller.default_engine_conf
engine_conf['name'] = '{{ task_list_name }}'
print 'engine paratemers:', engine_conf

# initiate the task list
db_name   = '{{ Scflex_database }}'
coll_name = '{{ Scflex_collection }}'
controller.init_task_list(db_name, coll_name, engine_conf)
controller. set_task_list(db_name, coll_name)

# add task example
example = """
controller.add_task_by_dict({
  'name'       : 'test-task',
  'timeout'    : 300,
  'executable' : '/bin/ls',
  'cmd_args'   : [{'all': ''}],
  'working_dir': '/home/kuanpern/'
})
"""
