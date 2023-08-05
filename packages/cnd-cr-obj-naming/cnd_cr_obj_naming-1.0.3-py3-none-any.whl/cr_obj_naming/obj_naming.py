from cnd_cr_object import CrObject
import hashlib


class ObjNaming(CrObject):
    consul_creds = {}

    def __init__(self, data, cnd_consul, md5_length, _print):
        super().__init__(_print)
        self._data = data
        self._cnd_consul = cnd_consul
        self._md5_length = md5_length

    def _value(self):
        base_string = f"aria{self._data['vra_id']}-{self._data['service_name']}-{self._data['env']}"
        hash_val = hashlib.md5(f"{base_string}-{self._data['deployment_id']}".encode())
        return f"{base_string}-{hash_val.hexdigest()[0:self._md5_length]}"

    def all(self):
        return self._cnd_consul.all()

    @property
    def data(self):
        return self._data
       
    @data.setter
    def data(self, my_data):
        self._data = my_data
        
    def save(self):
        self._data["name"] = self._value()
        self._print.trace_d(f'DeploymentId : {self._data["name"]}')
        self._cnd_consul.put(self._data["deployment_id"], self._data)
        return self._data["name"]

    def find_by_id(self, id):
        my_data = self._cnd_consul.get(id)
        self._print.trace_d(f'Raw data : {my_data}')
        return my_data
        
    def update(self):
        return self.save()
        
    def destroy(self):
        return self._cnd_consul.destroy(self._data["deployment_id"])
        
    def has_children(self):
        return False
        
    def find_relation(self):
        return []

