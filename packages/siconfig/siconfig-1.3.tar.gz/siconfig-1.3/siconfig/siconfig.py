from os import path, makedirs, remove
from siconfig.ErrorTypes import *
import re


class ConfigWork:
    def __init__(self, config_path: str):
        self.status = False
        self.cpath = config_path
    
    
    # ФУНКЦИИ-ДЕКОРАТОРЫ
    def init_check(func):
        def wrapper(*args, **kwargs):
            if not args[0].status:
                raise ConfigInitError
            return func(*args, **kwargs)
        return wrapper
    
    
    # ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ
    def update_result(self, res: dict, line: str):
        line = line.split('=')
        res[line[0]] = line[1].replace('\n', '')
    
    
    def r(self, fpath: str):
        return r"{}".format(fpath)
    

    # ОСНОВНЫЕ ФУНКЦИИ
    def init_config(self):
        folder, file = path.split(self.cpath)
        if folder != '':
            if not path.exists(self.r(folder)):
                makedirs(self.r(folder))
        if '.' not in file:
            raise WrongPathError
        self.status = True
    
    
    @init_check
    def create_config(self, section: str, **pairs):
        with open(self.r(self.cpath), 'w') as cconfig:
            cconfig.write(f'[{section}]\n')
            for key, value in pairs.items():
                cconfig.write(f'{key}={value}\n')
    
    
    @init_check
    def get_config(self):
        result = dict()
        regex = re.compile(r'\[(.*?)\]')
        with open(self.r(self.cpath), 'r') as cconfig:
            for line in cconfig.readlines():
                if regex.search(line) == None:
                    self.update_result(result, line)
        return result
    
    
    @init_check
    def get_key(self, key: str):
        result = str()
        regex = re.compile(r'\[(.*?)\]')
        with open(self.r(self.cpath), 'r') as cconfig:
            for line in cconfig.readlines():
                if regex.search(line) == None and key in line:
                    line = line.split('=')
                    result = line[1].replace('\n', '')
                    break
        return result
    
    
    @init_check
    def set_key(self, key: str, value: str):
        old_data = list()
        with open(self.r(self.cpath), 'r') as cconfig:
            for line in cconfig.readlines():
                if not key in line:
                    old_data.append(line.replace('\n', ''))
                else:
                    line = line.split('=')
                    old_data.append(f'{line[0]}={value}')
        remove(self.r(self.cpath))
        with open(self.r(self.cpath), 'w') as cconfig:
            for new_data in old_data:
                cconfig.write(f'{new_data}\n')
    
    
    @init_check
    def remove_key(self, key: str):
        old_data = list()
        with open(self.r(self.cpath), 'r') as cconfig:
            for line in cconfig.readlines():
                if not key in line:
                    old_data.append(line.replace('\n', ''))
        remove(self.r(self.cpath))
        with open(self.r(self.cpath), 'w') as cconfig:
            for new_data in old_data:
                cconfig.write(f'{new_data}\n')