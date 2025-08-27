from random import uniform
from json import dump, load, loads, dumps
from sensorStatusError import SensorStatusError
from datetime import datetime
import requests

URL_DE_BASE = "http://127.0.0.1:8000"
class Sensor:
    def __init__(self, id, status):
        self.id = id
        self. status = status
        self.last_value = None
    
    def simulate_data(self):
        if self.status != "On":
            raise SensorStatusError(f"Sensor can only operate if status is On. ({self.status=})")
        elif self.last_value is None:
            self.last_value = float(self.simulate_get_data_from_api())
    
    def display_data(self):
        return f"Last value of sensor {self.id} : {self.last_value}"
    
    """ def save_data(self):
        new_entry_registry = {"date" : str(datetime.now()), "value": self.last_value}
        current_registry = self.get_data_history()
        if current_registry is None:
            new_registry = [new_entry_registry]
        else:
            current_registry.append(new_entry_registry)
            new_registry = current_registry
        with open("sensor_value_registry_without_id.json", mode="w", encoding="utf-8") as write_file:
            dump(new_registry, write_file, indent=4)  """
            
    def get_data_history(self):
        try:
            with open("sensor_value_registry_without_id.json", mode="r", encoding="utf-8") as read_file:
                return load(read_file)
        except:
            print("File does not yet exist")
    
    """ def display_history(self):
        try:
            with open("sensor_value_registry.json", mode="r", encoding="utf-8") as read_file:
                data_history_json = load(read_file)
                #print(dumps(data_history_json, indent=2))
        except:
            print("File does not yet exist") """
    
    def simulate_get_data_from_api(self):
        reponse = requests.get("https://thingspeak.mathworks.com/channels/159156/feed.json").json()
        return reponse["feeds"][0]["field3"]
    
    """ def simulate_send_data_from_sensor_to_api(self):
        requests.post("https://httpbin.org/post", data={"value": str(self.last_value)}) """
    

def main():
    temperature_sensor = Sensor("A01", "On")
    temp_sensors = [Sensor("A04", "On"), Sensor("FR273W", "On"), Sensor("QSDF4", "On")]
    
    for sensor in temp_sensors:

        try:
            #temperature_sensor.simulate_data()
            sensor.simulate_data()
            requests.post(f"{URL_DE_BASE}/sensors/{sensor.id}/{sensor.last_value}")
        
        except SensorStatusError as ss_error:
            print(ss_error)
        
        else:
            #print(temperature_sensor.display_data())
            history_response : requests.Response = requests.get(f"{URL_DE_BASE}/history/{sensor.id}")
            print(history_response.content)
            last_value_response : requests.Response = requests.get(f"{URL_DE_BASE}/lastvalue/{sensor.id}")
            print(last_value_response.content)
            #print(type(last_value_response.content))

if __name__ == "__main__":
    main()