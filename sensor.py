from json import load
from sensorStatusError import SensorStatusError
import requests

URL_DE_BASE = "http://127.0.0.1:8000"
class Sensor:
    def __init__(self, id: str, status: str):
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
    
    def simulate_get_data_from_api(self):
        reponse = requests.get("https://thingspeak.mathworks.com/channels/159156/feed.json").json()
        return reponse["feeds"][0]["field3"]
    

def main():
    temp_sensors = [Sensor("A04", "On"), Sensor("FR273W", "On"), Sensor("QSDF4", "On")]
    
    for sensor in temp_sensors:

        try:
            sensor.simulate_data()
            requests.post(f"{URL_DE_BASE}/sensors/{sensor.id}/{sensor.last_value}")
        
        except SensorStatusError as ss_error:
            print(ss_error)
        
        else:
            history_response : requests.Response = requests.get(f"{URL_DE_BASE}/history/{sensor.id}")
            print(history_response.content)
            last_value_response : requests.Response = requests.get(f"{URL_DE_BASE}/lastvalue/{sensor.id}")
            print(last_value_response.content)

if __name__ == "__main__":
    main()