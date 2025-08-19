from random import uniform

class Sensor:
    def __init__(self, id, status):
        self.id = id
        self. status = status
        self.last_value = None
    
    def simulate_data(self):
        if self.last_value is None:
            self.last_value = uniform(0.0, 100.0)
    
    def display_data(self):
        return f"Last value of sensor {self.id} : {self.last_value}"
    
def main():
    temperature_sensor = Sensor("A01", "operational")
    temperature_sensor.simulate_data()
    print(temperature_sensor.display_data())

if __name__ == "__main__":
    main()