from Scflex_API import * # app, login_required, request
from flask_api import status

@app.route('/')
#@login_required
def home():
	return flask.render_template('pages/index.html', current_user = current_user)
# end def

@app.route('/pages/<pagename>')
#@login_required
def serve_page(pagename):
	template_html = 'pages/{pagename}.html'.format(pagename=pagename)
	return flask.render_template(template_html)
# end def
