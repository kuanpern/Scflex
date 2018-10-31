# API hook for fitbit heart rate Scfiex task registration
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from {{ flask_app_home }} import * # app, login_required, flask.request
import logging

# note: need better check code to report back to user

@app.route('/{{ url_prefix }}/add_task',        methods=['GET', 'POST'])
def add_task():
	content = flask.request.get_json()
	import {{ app_service_dir }}.{{ service_name }}.setup.task_manager as task_manager
	res = fitbit_heart.add_task(content)
	task_id = str(res)
	output = {"task_id": task_id}
	return flask.jsonify(res)
# end def

@app.route('/{{ url_prefix }}/activate_task',   methods=['GET', 'POST'])
def activate_task():
	content = flask.request.get_json()
	import {{ app_service_dir }}.{{ service_name }}.setup.task_manager as task_manager
	res = task_manager.activate_task(content)
	return flask.jsonify(res)
# end def

@app.route('/{{ url_prefix }}/deactivate_task', methods=['GET', 'POST'])
def deactivate_task():
	content = flask.request.get_json()
	import {{ app_service_dir }}.{{ service_name }}.setup.task_manager as task_manager
	res = task_manager.deactivate_task(content)
	return flask.jsonify(res)
# end def

@app.route('/{{ url_prefix }}/delete_task',     methods=['GET', 'POST'])
def delete_task():
	content = flask.request.get_json()
	task_name = content['task_name']
	import {{ app_service_dir }}.{{ service_name }}.setup.task_manager as task_manager
	res = task_manager.delete_task(task_name)

	output = {_: getattr(res, _) for _ in dir(res) if not(_.startswith('_'))}

	# note: MongoDB-specific. ObjectID not JSON-serializable
	# note: might switch to simplejson package that supports mongodb object later
	try:
		output['raw_result']['electionId']   = str(output['raw_result']['electionId'])
		output['raw_result']['opTime']['ts'] = str(output['raw_result']['opTime']['ts'])
	except Exception, e:
	logging.warning(repr(e))
	# end try

	return flask.jsonify(res)
# end def

