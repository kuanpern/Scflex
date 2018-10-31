#!/usr/bin/python
'''Scflex distributed computing engine'''
import uuid
import time
import yaml
import shlex
import datetime
import threading
import subprocess
import socket
import argparse
import numpy as np
from Scflex.externals.open_data_sciences.shorthand import require_inputs, mkdir_p, ConfigurationHandler, meta_parse_args
from Scflex.externals.open_data_sciences.common_utils import connect_sql_server
from pyspark import SparkContext

@require_inputs(['working_dir', 'executable', 'cmd_args', 'name'])
def func_executor(program_pars):
	# get an uuid label
	uuid_label = str(uuid.uuid4())

	# get hostname of the node which is assigned the task
	_hostname = socket.gethostname()

	# TODO: handle with 'extra_args'

	# check time-out
	timeout = program_pars['timeout'] if 'timeout' in program_pars.keys() else max_timeout
	timeout = min(timeout, max_timeout)

	# start building command line
	working_dir = program_pars['working_dir']
	exe_path    = program_pars['executable']
	cmd_args    = program_pars['cmd_args']
	cmd = exe_path + ' ' + cmd_args # TODO: safer way of doing this?

	# run the executable through shell
	response = {'hostname': _hostname, 'start_time': time.time()}
	start_time = time.time()
	try:
		response.update(shell_run_cmd(cmd, timeout_sec = timeout, cwd=working_dir))
	except Exception as e:
		response.update({
		  'name'   : name,
		  'uuid'   : uuid_label,
		  'stdout' : '',
		  'stderr' : repr(e),
		  'timeout': False,
		  'status' : 'failed',
		  'status_code': -1,
		  'info': {
		    'cpu_time': 0,
		    'ram'     : 0
		  }
		}) # end output
	# end try

	# collect status and time information
	if response['timeout'] == True:
		response['stderr'] += '\ntime-out error'
	# end if

	# write log file
	logfile_err_msg = ''
	try:
		write_log_file(program_pars['log_path'], response)
	except Exception as e:
		logfile_err_msg = '\nlog-file error: %s\n' % (repr(e),)
	# end try
	response['stderr'] += logfile_err_msg

	return response
# end def

def write_log_file(log_path, response):
	# write to log file
	with open(log_path, 'a') as fout:
		hostname   = response['hostname']
		start_time = datetime.datetime.utcfromtimestamp(response['start_time'])
		end_time   = datetime.datetime.utcfromtimestamp(response[  'end_time'])
		# write header
		fout.writelines('\n\n')
		fout.writelines('#'*80+'\n')
		fout.writelines('# TASK NAME: %s | UUID: %s\n' % (program_pars['name'], program_pars['uuid'],))
		fout.writelines('# hostname: %s | start-time: %s | end-time: %s\n' % (hostname, start_time, end_time,))
		# TODO: just json dump ?
		fout.writelines('#'*80+'\n')

		# write log
		fout.writelines('# stdout\n')
		fout.writelines(response['stdout'])
		fout.writelines('\n')
		fout.writelines('# sterr\n')
		fout.writelines(response['stderr'])
		fout.writelines('\n')
		fout.writelines('#'*80+'\n')
	# end with
# end def


# taken from http://stackoverflow.com/a/10768774
def kill_proc(proc, timeout):
	timeout['value'] = True
	proc.kill()
# end def


# taken from http://stackoverflow.com/a/10768774
def shell_run_cmd(cmd, timeout_sec, cwd):
	import resource
	start_time = time.time()
	start_mem = resource.getrusage(resource.RUSAGE_CHILDREN)

	timeout = {'value': False}
	proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
	# start timer (for process time-out)
	timer = threading.Timer(timeout_sec, kill_proc, [proc, timeout])
	timer.start()
	stdout, stderr = proc.communicate()
	timer.cancel()
	end_time = time.time()
	end_mem = resource.getrusage(resource.RUSAGE_CHILDREN)

	returncode = proc.returncode
	if returncode == 0:
		status = 'success'
	else:
		status = 'failed'
	# end if

	return {
	  'stdout' : stdout.decode('utf-8'),
	  'stderr' : stderr.decode('utf-8'),
	  'timeout': timeout['value'],
	  'status' : status,
	  'status_code': returncode,
      'start_time': start_time,
      'end_time'  : end_time,
	  'cpu_time': round(end_time - start_time, 2),
	  'ram'     : (end_mem.ru_maxrss - start_mem.ru_maxrss) / 1e3
	} # end output
# end def


def gen_set_content(response):
	sql_cmd = ''
	sql_cmd += '''status="{%s}"'''     % response['status']
	sql_cmd += '''uuid="{%s}"'''       % response['uuid']
	sql_cmd += '''failure_n={%s}'''    % str(response['failure_n'])
	sql_cmd += '''last_updated={%s}''' % str(response['last_updated'])
	sql_cmd += '''stdout="{%s}"'''     % compact_text(response['stdout'])
	sql_cmd += '''stderr="{%s}"'''     % compact_text(response['stderr'])
	sql_cmd += '''timeout={%s}'''      % str(response['timeout'])
	sql_cmd += '''status_code={%s}'''  % str(response['status_code'])
	sql_cmd += '''cpu_time={%s}'''     % str(response['cpu_time'])
	sql_cmd += '''ram={%s}'''          % str(response['ram'])
	return compact_text(sql_cmd)
# end def


# START HERE #
# parse arguments
parser = argparse.ArgumentParser(description='Scflex distributed computing main service engine')
parser.add_argument('--app',     required=True, help='Application name')
parser.add_argument('--conf',    required=True, help='path to configuration file (.yaml)')
parser.add_argument('--logdir',  required=True, help='log dir path')
parser.add_argument('--meta', help="meta parameter file list (.yaml)", nargs='+')

args = meta_parse_args(parser)
appName    = args['app']
conf_path  = args['conf']
log_dir    = args['logdir']

# set log file
####################################################################################
# TODO: to be refactor
import logging
import logging.handlers
mkdir_p(log_dir)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = '{log_dir}/{appName}.log'.format(log_dir=log_dir, appName=appName)
handler = logging.handlers.TimedRotatingFileHandler(logfile, when='D', interval=1) # could set to variables too
format_str = '%(asctime)s - %(levelname)-8s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(format_str, date_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
####################################################################################


# read main configuration file
__init_handler = ConfigurationHandler(source_type='yaml', source_path=conf_path)
init_configs = Struct(init_handler.Pars)
###############3
# TODO: verify if properly set
# c.f. https://stackoverflow.com/questions/32362783/how-to-change-sparkcontext-properties-in-interactive-pyspark-session
spark_conf = init_handler.Pars['spark'] if init_handler.Pars.has_key('spark') else {}
for key, val in spark_conf.items():
	SparkContext.setSystemProperty(key, val)
# end for
###############
del __init_handler

# intialize configuration handler
engine_conf_handler = ConfigurationHandler(source_type='yaml', source_path=conf_path)
engine_configs = Struct(engine_conf_handler.Pars)
# initialize a database connection
task_db_engine, task_db_conn = connect_sql_server(init_configs.task_db_conn_str)
# read task table name
task_table_name = init_configs.task_table_name

# initialize spark context
sc = SparkContext(appName=appName)
print('APP_ID: %s' % (sc.applicationId,))

# MAIN-LOOP
engine_conf_timestamp = -np.inf
while True:
	_now = time.time()
	logger.info('time now: ' + str(_now)) # TODO: better logging message

	# reload main configuration file
	if (_now - engine_conf_timestamp >= engine_configs.conf_refresh_interval):
		logger.info('refresh configuration handler')
		# refresh engine configs
		engine_conf_handler.refresh()
		engine_configs = Struct(engine_conf_handler.Pars)
		# - parse infinity
		if engine_configs.max_time_out == '.infinity':
			engine_configs.max_time_out = np.inf
		# end if

		# update timestamp
		engine_conf_timestamp = _now
	# end if

	task_db_conn
	batch_size = engine_configs.batch_size


	# Query from task table
	cols = ['name', 'last_updated', 'priority_r', 'working_dir', 'executable', 'cmd_args', 'log_path', 'extra_args']
	sql_cmd = """
	  SELECT {cols},
		priority_r*(last_updated-{cur_time}) as priority,
		(({cur_time}-last_updated) as timepast 
	  FROM {task_table_name}
	  WHERE timepast >= {min_repeat}) AND (status=="active") AND (failure_n<{max_failure_n}) 
	  ORDER BY priority LIMIT {nrows};
	""".strip().replace('\n', ' ')
	sql_cmd = sql_cmd.format(**{
		'cols'      : ', '.join(cols),
		'cur_time'  : time.time(),
		'nrows'     : engine_configs.batch_size,
		'min_repeat': engine_configs.min_repeat_interval,
		'max_failure_n'  : engine_configs.max_failure_n,
		'task_table_name': task_table_name
	})

	# fetching data
	cursor = conn.execute(sql_cmds)
	program_pars_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

	# if no task currently available
	if len(program_pars_list) == 0:
		logger.warning('no task to run, will sleep for a while.')
		time.sleep(engine_configs.hibernation_period_if_empty) # hibernate for one minute.
		continue
	# end if

	# distribute the task to different note to compute
	logger.info('distribute the task to worker nodes to compute ...')
	responses = sc.parallelize(program_pars_list).map(func_executor).collect()

	
	# update database with response
	# TODO: parallelization?
	# TODO: error handling
	for response in responses:
		sql_cmd = """
		  UPDATE {task_table_name}
		  SET {content}
		  WHERE name="{name}"; 
		""".format(**{
		  'name': engine_configs.min_repeat_interval,
		  'content'  : engine_configs.max_failure_n,
		  'task_table_name': task_table_name,
		  'content': gen_set_content(response)
		})
		sql_cmd = compact_text(sql_cmd)
		conn.execute(sql_cmd)
	# end for
# end while



''' # TODO: nice level thingy
import os
import psutil
import resource
import subprocess

def preexec_fn():
    pid = os.getpid()
    ps = psutil.Process(pid)
    ps.set_nice(10)
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))

print "mother pid", os.getpid()
p = subprocess.Popen(["./cpuhog.sh"], preexec_fn=preexec_fn)
p.wait()
print "mother still alive with pid", os.getpid()
'''



'''
for i in range(len(df)):
    try:
        df.iloc[i:i+1].to_sql(name="Table_Name",if_exists='append',con = Engine)
    except IntegrityError:
        pass #or any other action
'''
