from random import uniform
from sensorStatusError import SensorStatusError

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
    
    def display_data(self):
        return f"Last value of sensor {self.id} : {self.last_value}"
    
def main():
    temperature_sensor = Sensor("A01", "Off")
    try:
        temperature_sensor.simulate_data()
    except SensorStatusError as ss_error:
        print(ss_error)
    else:
        print(temperature_sensor.display_data())

if __name__ == "__main__":
    main()