import yaml
import os

def load_setting(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), '../../config/setting.yaml')
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print("setting.yaml not found. Make sire it exists in the congif/ filder.")
        return {}
    except yaml.YAMLError as e:
        print(f'YAML parasing error : {e}')
        return {}
    
