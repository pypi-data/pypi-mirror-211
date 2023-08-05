import consul
import json


class CndConsul():
	def __init__(self, host, port, token, path, print, scheme='https', verify=False):
		self._print = print
		self.consul_creds = {}
		self.consul_creds["host"] = host
		self.consul_creds["token"] = token
		self.consul_creds["path"] = path
		self.consul_creds["port"] = port
		self.consul_creds["scheme"] = scheme
		self.consul_creds["verify"] = verify
		self.consul = consul.Consul(
			host=self.consul_creds["host"],
			port=self.consul_creds["port"],
			token=self.consul_creds["token"],
			scheme=self.consul_creds["scheme"],
			verify=self.consul_creds["verify"]
		)

	def full_path(self, deployment_id=None):
		str = f'{self.consul_creds["path"]}/'
		if deployment_id is not None:
			str = f'{str}{deployment_id}'
		self._print.trace_d(f'Path : {str}')
		return str

	def all(self):
		index, paths = self.consul.kv.get(self.full_path(), recurse=True)
		self._print.trace_d(f'Returned value : {paths}')
		result = []
		for path in paths:
			result.append(json.loads(path["Value"]))
		self._print.trace_d(f'Item returned len : {len(result)}')
		return result

	def get(self, id=None):
		index, my_data = self.consul.kv.get(self.full_path(id))
		self._print.trace_d(f'Raw data : {my_data}')
		return json.loads(my_data['Value'])

	def put(self, id, data):
		return self.consul.kv.put(self.full_path(id), json.dumps(data, indent=4))

	def destroy(self, id):
		return self.consul.kv.delete(self.full_path(id))