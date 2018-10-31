from Scflex_API import * # app, login_required, flask.request

# JSON (data type application/json)
@app.route('/API/example_json', methods=['GET', 'POST'])
@login_required
def api_example_json():
	content = flask.request.get_json() # silent=True
	return flask.jsonify(content)
# end def

# URL Query parameter
@app.route('/API/example_urlQuery', methods=['GET'])
@login_required
def api_example_urlQuery():
	designation = flask.request.args.get('designation')
	username    = flask.request.args.get('username')
	template_html = 'pages/example_urlQuery_echo.html'
	return flask.render_template(template_html, designation=designation, username=username)
# end def

# Form input
@app.route('/API/example_formInput', methods=['POST'])
@login_required
def api_example_formInput():
	email    = flask.request.form.get('email')
	password = flask.request.form.get('password')
	template_html = 'pages/example_formInput_echo.html'
	return flask.render_template(template_html, email=email, password=password)
# end def
