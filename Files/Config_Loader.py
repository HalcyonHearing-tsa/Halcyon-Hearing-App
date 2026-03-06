from pathlib import Path
import json            
class ConfigLoader:
    def __init__(self, filepath= Path(__file__).resolve().parent ):
        self.filepath = filepath / 'config.json'
        self.configs = self.load_settings()
            
    def load_settings(self):        
        if not self.filepath.is_file():
            print("Json file not found.")
            return self.default_settings() 
        try:
            with  open(self.filepath) as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("Error reading JSON.")
            return self.default_settings() 
    def save_settings(self):
        with open(self.filepath, "w") as file:
            json.dump(self.configs, file, indent=4)
    def default_settings(self):
        default = {
            "is_light": True,
            "mode":[ "dark","light"],
            "tts_speed": 1,
            "phrases": ["Where is the bathroom?","I need water","Emergency!"]

        }
        self.settings = default
        self.save_settings()
        return default
