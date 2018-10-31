# low-level usage of schedule library
# - use only single thread. hard refresh for all upon any changes in the schedule jobs
# NOTE: TO BE REPLACED BY AIRFLOW

import common_utils as utils
import yaml
import time

from flask import jsonify
from flask import Flask

from Scflex_API import * # app, login_required, request
from flask_api import status
import shlex
import subprocess
import schedule
from multiprocessing import Process
import uuid

# receiver tasks
# consider authentication in the future
@app.route('/Scflex_controller/simple_scheduler_receiver', methods=['POST'])
def receive_cron_tasks():

	db_pars = configs
	db, db_client = utils.connect_mongoDB_server(db_pars)

	content = flask.request.get_json()
	# assign a uuid
	for i in range(len(content)):
		content[i]['uuid'] = uuid.uuid4()
	# end for

	# deactivate previous list
	db_client['Scflex_control']['cronjob_list'].update_many({'role': 'cronjob_list'}, {'$set': {'status': 'inactive'}})	

	# insert new list
	doc = new_doc(); doc['content'] = content
	ans = db_client['Scflex_control']['cronjob_list'].insert_one(doc)
	
	return ans
# end def

# export tasks
# consider authentication in the future
@app.route('/Scflex_controller/simple_scheduler_export', methods=['GET'])
def export_cron_tasks(): # template of new financial record document
	tasks = schedule_manager().list_tasks()
	return jsonify(tasks)
# end def

def is_processed(uuid):
	# need a mechanism to record processed jobs
#	doc = db_client['Scflex_control']['cronjob_list'].find({'role': 'cronjob_list'}).sort('last_updated', pymongo.DESCENDING).limit(1)
#	sel = [item for item in doc['content'] if item['uuid'] == uuid]
#	if len(sel) != 1:
#		# todo: report
#		pass
#	# end if
#	sel = sel[0]
	return False
# end def

def run_cmd(cmd, uuid):
	if is_processed(uuid): return
	p = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE)
	# get output status
	output, err = p.communicate()
	rc = p.returncode
	# update to database
	ans = db_client['Scflex_control']['cronjob_list'].update_one(
	  {'role': 'cronjob_list', 'status': 'active', 'content.uuid': uuid},
	  {'$set': {'content.$.last_status': rc, 'content.$.last_run': time.time()}
	}) # end update
# end def

def start_schedule(execlines, interval = None):
	assert type(inputs) == dict
	if interval == None: interval = 1
	# "refresh" schedule object
	schedule.clear()

	# parse and populate schedule object
	for execline in execlines:
		exec(execline)
	# end for

	# actually run
	while True:
		schedule.run_pending()
		time.sleep(interval)
	# end while
# end def

class schedule_manager:

	def __init__(self, interval = 1):
		self.interval = interval
	# end def

	def start_tasks(self):
		# get and parse tasks
		tasks = self.list_tasks()
		execlines = self.parse_inputs(tasks)
		if len(execlines) == 0: return

		# actually run
		if self.proc: self.proc.terminate()
		self.proc = Process(target=start_schedule, args=(execlines, self.interval,))
		self.proc.start(); self.proc.join()
	# end def

	def list_tasks(self):
		doc = db_client['Scflex_control']['cronjob_list'].find_one({'role': 'cronjob_list', 'status': 'active'})
		return doc['content']
	# end def

	def parse_inputs(self, inputs):
		execlines = []
		for var in inputs:
			# check inputs
			_unit = var['unit']
			if _unit not in ['minute', 'hour', 'day', 'week']:
				return {'status': 'failed', 'errors': ['unit not understood']}
			if _unit in ['day', 'week']:
				if _time == None:
					return {'status': 'failed', 'errors': ['must have time']}
			if _unit == 'week':
				if _weekday == None:
					return {'status': 'failed', 'errors': ['must have weekday']}

			# generate scheduling commands
			if _unit == 'minute':
				execline = 'schedule.every(%d).minutes.do(run_cmd, "%s", "%s")'      % map(var.get, ['freq','cmd','uuid'])
			elif _unit == 'hour':
				execline = 'schedule.every(%d).hour.do(run_cmd, "%s", "%s")'         % map(var.get, ['freq','cmd','uuid'])
			elif _unit == 'day':
				execline = 'schedule.every(%d).day.at("%s").do(run_cmd, "%s", "%s")' % map(var.get, ['freq','freq','cmd','uuid'])
			elif _unit == 'week':
				execline = 'schedule.every(%d).%s.at("%s").do(run_cmd, "%s", "%s")'  % map(var.get, ['freq','weekday','time','cmd','uuid'])
			# end if
			execlines.append(execline)
		# end for
		return execlines
	# end def
# end class
