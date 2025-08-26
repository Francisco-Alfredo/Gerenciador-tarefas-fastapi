from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from fast_zero.schemas import (
    MessageSchema,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()

app.mount('/coverage', StaticFiles(directory='htmlcov'), name='coverage')


database = []


@app.get('/', status_code=200, response_model=MessageSchema)
def read_root():
    return {'message': 'Welcome to the Fast Zero API!'}


@app.post('/users', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get('/users', response_model=UserList)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=404, detail='User not found')

    index = user_id - 1
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[index] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=MessageSchema)
def delete_user(user_id: int):
    if user_id < len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')
    database.pop(user_id - 1)
    return {'message': 'User deleted successfully'}
