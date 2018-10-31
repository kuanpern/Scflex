# Flask settings
import json
from flask import Flask, render_template, send_from_directory, request
from flask_cors import cross_origin
app = Flask(__name__, static_url_path='/static')
# Scube settings
from Scube_controller_dashboard_helpers import *

@app.route('/getUpdateStatus/<name>')
@cross_origin(origin='*')
def sendUpdateStatusData(name):
	dbname = '{name}UpdateStatus'.format(name=name)
	data = get_UpdateStatusData(db_name=dbname)
	return json.dumps(data)
# end def



'''
@app.route('/')
def index():
	return send_from_directory('static', 'index.html')
# end def

@app.route('/hello')
def hello_world():
	return 'Hello World'
# end def

@app.route('/hello/<name>')
def hello_name(name):
	return 'Hello %s' % name
# end def

@app.route('/blog/<int:postID>')
def show_blog(postID):
	return 'Blog Number %d' % postID
# end def

@app.route('/rev/<float:revNo>')
def show_revision(revNo):
	return 'Revision number %f' % revNo
# end def
'''

if __name__ == '__main__':
	app.run(port=5001)
# end if
