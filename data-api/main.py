import utils.simulation_utils as sim
from fastapi import FastAPI, Form, Response
import logging
from logging.config import dictConfig
from log_config import log_config



dictConfig(log_config)
logger = logging.getLogger("Trainer")

signal = sim.signals_case_generation(n_transition_steps=500)

app = FastAPI()

# TODO include params in a config file
prod_url = 'http://prod-api:5000/'
trainer_url = 'http://trainer:5000/'

@app.get("/health")
async def health_root():
    logger.info("Data Simalutor: Health request received.")
    return "Data Simalutor is online."


@app.get("/timesteps")
async def data(initial_step: int):
    data = sim.timesteps_generator(signal, start_timestep=initial_step)

    # frame_file = io.BytesIO(frame) # yes, that is enough
    # rsp = requests.post(url, ..., files={'img': frame_file}) 

    data_bytes = data.tobytes() # numpy array to bytes object
    # rsp = requests.post(url, ..., data=frame_bytes) 
    headers = {'Content-Disposition': 'inline; filename="timesteps"'}
    return Response(data_bytes, headers=headers, media_type='image/png')


@app.post('/listen')
async def _file_upload(
        # my_file: UploadFile = File(...),
        first:  str = Form(...),
        second: str = Form(...),
):
    print(f'logger> Trainer: Received message from {second}')
    reply = f'{round(float(first)*10/2,0)}'

    return {
        # "name": my_file.filename,
        "Number": reply,
    }


# frame_bytes = frame_encoded.tobytes() # numpy array to bytes object
# rsp = requests.post(url, ..., data=frame_bytes) 