#!/usr/bin/python
import sys
import yaml
import common_utils as utils
from Scflex.utils.task_management_utils import Scflex_controller
from shorthand import require_inputs
import logging
logging.basicConfig()

# read mongodb credential file
mongo_cred_file = '{{ mongodb_credential_file }}'
db_pars = yaml.load(open(mongo_cred_file))

# initiate the controller
controller = Scflex_controller(db_pars)

# initiate the task list
<<<<<<< HEAD
db_name   : {{ Scflex_database }}
coll_name : {{ Scflex_collection }}
controller.set_task_list(db_name, coll_name)

# set arguments
install_dir = '{{ install_dir }}'
cmd = '{install_dir}/package/service_venv/bin/python {install_dir}/package/bin/main.py'
cmd = cmd.format(install_dir=install_dir)
meta_dir = '{install_dir}/templates/'
meta_files = '{meta_dir}/pars_1.yaml {meta_dir}/pars_2.yaml {meta_dir}/pars_3.yaml'
=======
db_name   = '{{ Scflex_database }}'
coll_name = '{{ Scflex_collection }}'
controller.set_task_list(db_name, coll_name)

# set arguments
install_dir = '{{ install_dir }}/{{ application_name }}'
meta_dir = '{install_dir}/templates/'
# --- modify accordingly --- #
cmd = '{install_dir}/package/service_venv/bin/python {install_dir}/package/bin/main.py'
cmd = cmd.format(install_dir=install_dir)
meta_files = '{meta_dir}/pars_1.yaml {meta_dir}/pars_2.yaml {meta_dir}/pars_3.yaml'
# --- end modify accordingly --- #
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
meta_files = meta_files.format(meta_dir=meta_dir)
working_dir = '{install_dir}/workspace'.format(install_dir=install_dir)

# add task example
<<<<<<< HEAD
@require_inputs(['task_name', 'task_var1', 'task_var2', 'task_var3', 'timeout'])
=======
@require_inputs(['task_name', 'task_var1', 'task_var2', 'task_var3', 'timeout']) # <-- modify accordingly
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
def add_task(input_vars):
	res = controller.add_task_by_dict({
	  'name'       : input_vars['task_name'],
	  'timeout'    : input_vars['timeout'],
	  'executable' : cmd,
	  'cmd_args'   : [
<<<<<<< HEAD
	    {'meta': meta_files}, 
	    {'arg1'    : input_vars['task_var1']},
            {'arg1'    : input_vars['task_var2']},
            {'arg1'    : input_vars['task_var3']},
=======
	    {'meta': meta_files},
	    # --- modify accordingly --- #
	    {'arg1': input_vars['task_var1']},
	    {'arg2': input_vars['task_var2']},
	    {'arg3': input_vars['task_var3']},
	   # --- end modify accordingly --- #
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
  	  ],
  	  'working_dir': working_dir
	})
	return res
# end def

@require_inputs(['task_name'])
def activate_task(input_vars):
<<<<<<< HEAD
        return controller.activate_task_program(input_vars['task_name'])
=======
	return controller.activate_task_program(input_vars['task_name'])
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
# end def

@require_inputs(['task_name'])
def deactivate_task(input_vars):
<<<<<<< HEAD
        return controller.deactivate_task_program(input_vars['task_name'])
=======
	return controller.deactivate_task_program(input_vars['task_name'])
>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
# end def

@require_inputs(['task_name'])
def delete_task(input_vars):
<<<<<<< HEAD
        return controller.delete_task_program(input_vars['task_name'])
# end def
=======
	return controller.delete_task_program(input_vars['task_name'])
# end def

>>>>>>> e009115e2b8660f291d8a3c8db71e01d39525aa5
