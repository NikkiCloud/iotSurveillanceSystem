
from fastapi import FastAPI
from datetime import datetime
from json import dump, load

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Home Surveillance System"}

@app.get("/history/{sensor_id}")
async def get_sensor_data_history(sensor_id : str):
    pass

@app.post("/sensors/{sensor_id}/{value_measured}")
async def send_sensor_data(sensor_id: str, value_measured: float):
    await save_sensor_data(sensor_id, value_measured)
    return {"sensor id" : sensor_id, "value_measured" : value_measured}



async def save_sensor_data(sensor_id: str, value_measured: float):
    new_entry_registry = {"date" : str(datetime.now()), "value": value_measured}
    current_registry = await obtain_data_history()
    if current_registry is None:
        new_registry = {sensor_id : [new_entry_registry]}
    else:
        current_registry[sensor_id].append(new_entry_registry)
        new_registry = current_registry
    with open("sensor_value_registry.json", mode="w", encoding="utf-8") as write_file:
        dump(new_registry, write_file, indent=4)
    print("Data has been saved", flush=True)
    return {"message": "Data has been saved"}

async def obtain_data_history():
    try:
        with open("sensor_value_registry.json", mode="r", encoding="utf-8") as read_file:
            return load(read_file)
    except:
        print("File does not yet exist")