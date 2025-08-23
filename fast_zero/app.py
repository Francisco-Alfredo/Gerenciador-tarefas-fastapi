from fastapi import FastAPI

from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/coverage", StaticFiles(directory="htmlcov"), name="coverage")

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Fast Zero API!'}
