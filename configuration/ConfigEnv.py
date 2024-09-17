import os
import yaml
from configuration.ConfigDecryptor import ConfigDecryptor

class ConfigEnv:
    def __init__(self):
        self.configEnv = None
        self.decryptor = None

    def load_config(self, env):
        app_dir = os.path.abspath(os.path.dirname(__file__))
        config_path = os.path.join(app_dir, 'config.yaml')
        self.decryptor = ConfigDecryptor(config_path=config_path)

        with open(config_path, 'r') as file:
            self.configEnv = yaml.safe_load(file).get(env, {})

    def get(self, *keys, default=None):
        if len(keys) == 1:
            key = keys[0]
            matches = self.search_key(key)
            if len(matches) == 1:
                value = list(matches.values())[0]
                return self.decryptor.decrypt_value(value)
            elif len(matches) > 1:
                raise KeyError(f"Duplicate key '{key}' found. Specify the parent key.")
            else:
                return default
        else:
            value = self.get_with_parent(*keys, default=default)
            return self.decryptor.decrypt_value(value)

    def search_key(self, key):
        result = {}
        def recursive_search(d, path=[]):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k == key:
                        result["/".join(path + [k])] = v
                    recursive_search(v, path + [k])
        recursive_search(self.configEnv)
        return result

    def get_with_parent(self, *keys, default=None):
        value = self.configEnv
        for key in keys:
            value = value.get(key)
            if value is None:
                return default
        return value

# Instancia global de configuración
configEnv = ConfigEnv()