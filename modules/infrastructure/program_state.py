import json
import os
from typing import Union
from pathlib import Path


class ProgramState:
    def __init__(self, store_backup: Union[str, Path] = '.program.state~',
                 store_file: Union[str, Path] = '.program.state'):
        self._state = {}
        self._store_backup = store_backup
        self._store_file = store_file

    def add_to_param_value(self, param: str, value):
        self._state[param] = value

        return self

    def get_name_store_file(self):
        return self._store_file

    def get(self, param: str):
        return self._state[param]

    def dump(self):
        try:
            with open(self._store_backup, 'w') as f:
                json.dump(self._state, f)

            os.rename(self._store_backup, self._store_file)
        except Exception as e:
            print(str(e))
            os.remove(self._store_file)

    def program_finish(self):
        os.remove(self._store_file)

    def get_state_json(self):
        if os.path.isfile(self._store_backup):
            os.remove(self._store_backup)

        if os.path.isfile(self._store_file):
            with open(self._store_file, 'r') as f:
                state = json.load(f)
                self._state = state

        return self

    def delete_state(self):
        if os.path.isfile(self._store_backup):
            os.remove(self._store_backup)

        if os.path.isfile(self._store_file):
            os.remove(self._store_file)

    @staticmethod
    def get_states_from_directory(path_to_directory: Union[str, Path]):
        name_files = []
        for name_file in os.listdir(path_to_directory):
            if name_file.find('~') != -1:
                os.remove(Path(path_to_directory, name_file))
            else:
                name_files.append(name_file)

        return name_files

