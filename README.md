## Scflex: A flexible distributed engine framework powered by Apache Spark & MongoDB


### Installation
#### Dependencies
 - Apache Spark
 - MongoDB
 - HADOOP YARN (for High Availabilty)

#### set PYTHONPATH
```
$ export PYTHONPATH=$PYTHONPATH:/home/kuanpern/Scflex/Scflex-master
```

1. Ensure that "spark-submit" is on the PATH variable.
2. Ensure HADOOP cluster is running properly

Optionally, install the task monitoring server.
 - Refer to Scflex/controls/README.md

#### Add new service (task list) to the engine
```
$ # use interactive session with
$ ./bin/interactive_add_service
```

### Roadmap
 - Socket-based logging system
 - Dashboard to monitor the job and node status 
 - run python by module import / thread-based processing
