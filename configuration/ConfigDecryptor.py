from cryptography.fernet import Fernet
import yaml

class ConfigDecryptor:
    def __init__(self, key_path="encryption/secret.key", config_path="configuration/config.yaml"):
        self.key_path = key_path
        self.config_path = config_path
        self.key = self.load_key()
        self.encrypted_config = self.load_encrypted_config()

    def load_key(self):
        with open(self.key_path, "rb") as key_file:
            return key_file.read()

    def load_encrypted_config(self):
        with open(self.config_path, "r") as config_file:
            return yaml.safe_load(config_file)

    def decrypt_data(self, encrypted_data):
        f = Fernet(self.key)
        decrypted_data = f.decrypt(encrypted_data.encode()).decode()
        return decrypted_data

    def get_decrypted_config(self):
        return {k: self.decrypt_data(v) for k, v in self.flatten_dict(self.encrypted_config).items()}

    def flatten_dict(self, d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def decrypt_value(self, value):
        if isinstance(value, str) and value.startswith("gAAAA"):
            return self.decrypt_data(value)
        return value