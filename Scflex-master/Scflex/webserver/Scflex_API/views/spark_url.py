from Scflex_API import * # app, login_required, request

@app.route('/Scflex_controller/spark_ui', methods=['GET'])
def get_spark_ui_url():
	return configs['spark_ui_url']
# end def

