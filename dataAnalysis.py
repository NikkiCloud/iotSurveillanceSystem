import pandas as pd
from json import load

class DataAnalysis:
    def __init__(self, data_file_pathX):
        self.data_file_path = data_file_pathX
        self.data = pd.read_json(data_file_pathX)

    def load_data(self):
        try:
            with open(self.data_file_path, mode="r", encoding="utf-8") as w_file:
                return load(w_file)
        except:
            print("Can't find this file")


    def convert_dict_to_dataframe(self):
        data_json = self.load_data()
        data_df = pd.DataFrame(data_json["A01"])
        return data_df
    
    def get_sum(self):
        return self.convert_dict_to_dataframe()["value"].sum()

    def get_average(self):
        return self.convert_dict_to_dataframe()["value"].mean()
    
    def get_minimum(self):
        return self.convert_dict_to_dataframe()["value"].min()

    def get_maximum(self):
        return self.convert_dict_to_dataframe()["value"].max()   


def main():
    data_temp_sensors = DataAnalysis("./sensor_value_registry.json")
    print(data_temp_sensors.get_average())
    print(data_temp_sensors.get_sum())
    print(data_temp_sensors.get_minimum())
    print(data_temp_sensors.get_maximum())


if __name__ == "__main__":
    main()