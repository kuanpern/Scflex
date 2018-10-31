# Scube settings
from shorthand import *
import Scube
import Scube.utils
import Scube.conf
import pandas as pd
# configuration
conf_path = Scube.conf.conf_path
conf_handler = Scube.utils.configuration_handler(conf_path)
# connect to mongoDB
mongodb_pars = conf_handler.Pars['database']['mongodb']
db, client = Scube.utils.database_utils.common_utils.connect_mongoDB_server(mongodb_pars)


# for now, all systems use the same status framework
def get_UpdateStatusData(db_name, colnames = ['market', 'symbol', 'priority', 'failures', 'last_record', 'last_updated', 'last_success', 'last_failure', 'active'], na_filler = '-'):
	# get the data and proper formatting
	status_df = pd.DataFrame(list(db[db_name].find()))
	for colname in ['last_failure', 'last_success', 'last_updated']:
		status_df[colname] = map(timestamp2datetime, status_df[colname])
	# end for
	
	status_out = status_df[colnames]
	status_out = status_out.fillna(na_filler)
	status_out = status_out.sort_values(by = ['last_updated'], ascending=[False])

	# formatting and return
	content = status_out.to_records(index=None).tolist()
	return {'data': content}	
# end def	



