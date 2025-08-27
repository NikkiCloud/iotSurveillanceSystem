
from fastapi import FastAPI, HTTPException
from datetime import datetime
from json import dump, load

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Home Surveillance System"}

@app.get("/lastvalue/{sensor_id}")
async def get_last_value(sensor_id : str):
    data_history = await obtain_data_history(sensor_id)
    return data_history[-1]["value"]

@app.get("/history/{sensor_id}")
async def get_sensor_data_history(sensor_id : str):
    try:
        with open(f"sensor_{sensor_id}_registry.json", mode="r", encoding="utf-8") as read_file:
            return {"history" : load(read_file)}
    except:
        raise HTTPException(status_code=404, detail="File does not exist")


@app.post("/sensors/{sensor_id}/{value_measured}")
async def send_sensor_data(sensor_id: str, value_measured: float):
    await save_sensor_data(sensor_id, value_measured)
    return {"sensor id" : sensor_id, "value_measured" : value_measured}



async def save_sensor_data(sensor_id: str, value_measured: float):
    new_entry_registry = {"date" : str(datetime.now()), "value": value_measured}
    current_registry = await obtain_data_history(sensor_id)
    if current_registry is None:
        new_registry = [new_entry_registry]
    else:
        current_registry.append(new_entry_registry)
        new_registry = current_registry
    with open(f"sensor_{sensor_id}_registry.json", mode="w", encoding="utf-8") as write_file:
        dump(new_registry, write_file, indent=4) 
    
    return {"message": "Data has been saved"}

async def obtain_data_history(sensor_id: str):
    try:
        with open(f"sensor_{sensor_id}_registry.json", mode="r", encoding="utf-8") as read_file:
            return load(read_file)
    except:
        raise HTTPException(status_code=404, detail="File does not exist")
