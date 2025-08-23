from random import uniform
from json import dump, load, loads, dumps
from sensorStatusError import SensorStatusError
from datetime import datetime

class Sensor:
    def __init__(self, id, status):
        self.id = id
        self. status = status
        self.last_value = None
    
    def simulate_data(self):
        if self.status != "On":
            raise SensorStatusError(f"Sensor can only operate if status is On. ({self.status=})")
        elif self.last_value is None:
            self.last_value = uniform(0.0, 100.0)
            self.save_data()
    
    def display_data(self):
        return f"Last value of sensor {self.id} : {self.last_value}"
    
    def save_data(self):
        new_entry_registry = [{"date" : str(datetime.now()), "value": self.last_value}]
        current_registry = self.get_data_history()
        if current_registry is None:
            new_registry = {self.id : new_entry_registry}
        else:
            current_registry[self.id].append(new_entry_registry)
            new_registry = current_registry
        with open("sensor_value_registry.json", mode="w", encoding="utf-8") as write_file:
            dump(new_registry, write_file)
    
    def get_data_history(self):
        try:
            with open("sensor_value_registry.json", mode="r", encoding="utf-8") as read_file:
                return load(read_file)
        except:
            print("File does not yet exist")
    
    def display_history(self):
        try:
            with open("sensor_value_registry.json", mode="r", encoding="utf-8") as read_file:
                data_history_json = load(read_file)
                print(dumps(data_history_json, indent=2))
        except:
            print("File does not yet exist")
    
def main():
    temperature_sensor = Sensor("A01", "On")
    try:
        temperature_sensor.simulate_data()
    except SensorStatusError as ss_error:
        print(ss_error)
    else:
        print(temperature_sensor.display_data())
        temperature_sensor.display_history()

if __name__ == "__main__":
    main()