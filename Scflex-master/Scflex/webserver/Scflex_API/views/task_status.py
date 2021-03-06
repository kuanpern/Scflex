import htmlmin
import datetime
import numpy as np
import pandas as pd
pd.set_option('display.max_colwidth', -1)
import common_utils as utils
import yaml
import time
from copy import deepcopy
import tempfile
from bs4 import BeautifulSoup
import lxml

from flask import jsonify
from flask import Flask

from Scflex_API import * # app, login_required, request
from flask_api import status

@app.route('/Scflex_controller/load_task_lists', methods=['GET'])
def load_task_lists():
		# initiate database connection
#		db_pars_path = '/home/scube_backend/.keys/mongodb_pars.yaml' # note: hardcoded !
#		db_pars = yaml.load(open(db_pars_path))
		db_pars = configs
		db, db_client = utils.connect_mongoDB_server(db_pars)

		# query scflex control databse
		ans = db_client['Scflex_control']['task_list_monitoring'].find({"role":"task_list_info"})
		ans = list(ans)
		if len(ans) == 0: ""

		# get task list name
		task_list_names = [doc['db_name']+'/'+doc['coll_name'] for doc in ans]

		# make the html
		soup = BeautifulSoup("", 'lxml')
		for name in task_list_names:
				new_tag = soup.new_tag('option')
				new_tag.attrs['value'] = name
				label = ' - '.join(name.split('/'))
				new_tag.insert(0, label)
				soup.insert(0, new_tag)
		# end for

		return str(soup)
# end def

def date_formatter(s):
	return datetime.datetime.fromtimestamp(int(s)).isoformat(sep=' ')
# end def


def innerHTML(element):
	return element.decode_contents(formatter="html")
# end def

@app.route('/Scflex_controller/<out_format>/<db_name>/<coll_name>', methods=['GET'])
def task_status_to_html(out_format, db_name, coll_name, outfile = None):
	df = get_task_statuses(db_name, coll_name)

	cols = ['name', 'status', 'priority_r', 'last_updated', 'last_status', 'last_success', 'last_failure', 'failure_n', 'last_error', 'last_output']
	df = df[cols]

	assert out_format in ['html', 'csv']
	if out_format == 'html':
		# make last_output and last_error text into link
		for col in ['last_output', 'last_error']:
			contents = df[col].values
			for i in range(len(contents)):
				if str(contents[i]).strip() != '':
					contents[i] = '<a href="#" data-msg="'+contents[i]+'" onclick=show_msg($(this).data("msg"))>show</a>'
				# end if
			# end for
			df[col] = contents
		# end for

		html = df.to_html(index=False, escape=False)
		# get the content only
		soup = BeautifulSoup(html, 'lxml')
		html = innerHTML(soup.find('table'))
		output = htmlmin.minify(html, remove_empty_space=True)
	elif out_format == 'csv':
		return df.to_csv()
	# end if

	if outfile == None:
		return html
	else:
		open(outfile, 'w').writelines(html)
	# end if
# end def

def get_task_statuses(db_name, coll_name):
	# need stronger security check here -> ensure it's a task list

	# initiate database connection
	db_pars_path = '/home/scube_backend/.keys/mongodb_pars.yaml' # note: hardcoded !
	db_pars = yaml.load(open(db_pars_path))
	db, db_client = utils.connect_mongoDB_server(db_pars)

	# get all tasks from database
	cur_time = date_formatter(time.time())
	tasks = list(db_client[db_name][coll_name].find({'role': 'task'}))
	names = [_['name']   for _ in tasks]
	tasks = [_['status'] for _ in tasks]

	output = []
	for i in range(len(tasks)):
		task = deepcopy(tasks[i])
		res = task.pop('last_response')
		res.pop('status_code')
		duration = res.pop('info')['duration']

		# add extra information
		task['name'] = names[i]
		task['duration'] = duration
		# combine with other task info
		out = info = {'last_'+key:val for key, val in res.items()}
		out.update(task)
		output.append(out)
	# end for

	df = pd.DataFrame(output)

	# date format
	date_cols = ['last_failure', 'last_success', 'last_updated']
	for _col in date_cols:
		df[_col] = map(date_formatter, df[_col])
	# end for

	# organize columns
	cols = ['name', 'last_updated', 'last_success', 'last_failure', 'failure_n', 'last_status', 'last_output', 'last_error', 'status', 'priority_r']
	# cheap fix for missing columns
	for col in cols:
		if col not in df.columns:
			df[col] = 'N/A'
		# end if
	# end for

	df = df[cols]

	db_client.close()
	return df
# end def
