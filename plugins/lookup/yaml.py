import os
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.parsing.vault import VaultSecret

class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        if len(terms) != 2:
            raise AnsibleError("yaml lookup requires exactly 2 arguments: file_path and key")

        file_path, key_name = terms

        # Expand tilde (~) and environment variables
        file_path = os.path.expanduser(os.path.expandvars(file_path))

        if not os.path.exists(file_path):
            raise AnsibleError(f"YAML file not found: {file_path}")

        try:
            # Check if the file is encrypted
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                if first_line.startswith('$ANSIBLE_VAULT;'):
                    # Decrypt the file using the Vault mechanism
                    vault_secrets = self._loader._vault.secrets
                    with open(file_path, 'rb') as encrypted_file:
                        decrypted_content = self._loader._vault.decrypt(encrypted_file.read(), vault_secrets)
                else:
                    # Load the file as plain text
                    with open(file_path, 'r') as yaml_file:
                        decrypted_content = yaml_file.read()

            # Parse the decrypted content as YAML
            data = self._loader.load(decrypted_content, file_path)

        except Exception as e:
            raise AnsibleError(f"Error reading or decrypting YAML file {file_path}: {e}")

        # Extract the requested key
        if key_name not in data:
            raise AnsibleError(f"Key '{key_name}' not found in YAML file {file_path}")

        return [data[key_name]]