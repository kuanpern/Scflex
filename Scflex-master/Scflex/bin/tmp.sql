CREATE TABLE task_table (
	status TEXT, 
	uuid TEXT, 
	name TEXT, 
	failure_n BIGINT, 
	date_created DATETIME, 
	last_updated FLOAT, 
	priority_r FLOAT, 
	working_dir TEXT, 
	executable TEXT, 
	cmd_args TEXT, 
	stdout TEXT, 
	stderr TEXT, 
	timeout FLOAT, 
	status_code FLOAT, 
	cpu_time FLOAT, 
	ram FLOAT, 
	log_path TEXT,
	extra_args TEXT,
	PRIMARY KEY (name)
);
CREATE INDEX ix_task_table_index ON task_table ("name");

