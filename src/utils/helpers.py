import os
import yaml

def load_config(config_path: str = "config.yaml") -> dict:
    """Loads configuration from a YAML file.
    
    If the file does not exist in the current working directory, 
    tries to locate it in the parent directories of the script.
    """
    if not os.path.exists(config_path):
        # Try to locate config.yaml relative to this script's directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        config_path = os.path.join(base_dir, "config.yaml")
        
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading configuration from {config_path}: {e}")
        return {}
