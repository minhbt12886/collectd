<LoadPlugin python>
    Globals true
</LoadPlugin>
<Plugin python>
    ModulePath "/etc/collectd/python-modules/"
    LogTraces true
    Import "mongodb_extra"
    <Module mongodb_extra>
        Host "127.0.0.1"
        Port "27017"
        User "*******"
        Password "*******"
        Database "admin"
    </Module>
</Plugin>
#!/usr/bin/python
from pymongo import MongoClient
import collectd

def config_func(config):
	for node in config.children:
		if node.key == 'Port':
			global MONGO_PORT
			MONGO_PORT = int(node.values[0])
		elif node.key == 'Host':
			global MONGO_HOST
			MONGO_HOST = node.values[0]
		elif node.key == 'User':
			global MONGO_USER
			MONGO_USER = node.values[0]
		elif node.key == 'Password':
			global MONGO_PASSWORD
			MONGO_PASSWORD = node.values[0]
		elif node.key == 'Database':
			global MONGO_DB
			MONGO_DB = node.values[0]
		else:
			collectd.warning("mongodb-extra plugin: Unkown configuration key %s" % node.key)

def read_func():
#	collectd.info("%s %s %s %s %s %s" % (MONGO_USER,MONGO_PASSWORD,MONGO_HOST,MONGO_PORT,MONGO_DB))
 	uri = "mongodb://%s:%s@%s:%s/?authSource=%s" % (MONGO_USER,MONGO_PASSWORD,MONGO_HOST,MONGO_PORT,MONGO_DB)
 	client = MongoClient(uri)
	dbs=client.database_names()
	for db in dbs:
		collections=client[db].collection_names()
		for collection in collections:
			instance_name="%s-%s" % (db,collection)
			data = collectd.Values(plugin='mongo_extra', plugin_instance=instance_name, type='gauge', type_instance='total_documents')
			data.dispatch(values=[client[db][collection].count()])

collectd.register_config(config_func)
collectd.register_read(read_func
