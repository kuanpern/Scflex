#!/usr/bin/python
'''still in development, untested !'''

# connect to HDFS file system
hdfs_host = 'localhost'
hdfs_port = '50070'
hdfs_url  = 'http://{host}:{port}'.format(host = hdfs_host, port = hdfs_port)
hdfs_user = 'hadoop'

from hdfs import InsecureClient
client = InsecureClient(hdfs_url, user=hdfs_user)

# need a receptionist node
# host a nginx server
# best to have a hostname
# listening to log message 

# receive socket log message and redirect to hdfs
from socket import *
receptionist_host = "Scflex_receptionist"
receptionist_port = 13000
buf  = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

# generate initial file
cur_date = current_date()
hdfs_path = new_hdfs_path(cur_date)

c = 0
while True:
	c += 1
	(data, addr) = UDPSock.recvfrom(buf)
	client.write(hdfs_path, data, buffersize = buf, append = True)

	if c % 10000:
		cur_date_new = current_date()
		if cur_date_new != cur_date: # new day
			cur_date = cur_date_new
			hdfs_path = new_hdfs_path(cur_date)
		# end if

		c = 0 # reset counter
	# end if
# end while
UDPSock.close()

