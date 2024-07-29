import os
from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi_pagination import Page, add_pagination, paginate

from reqres_app.models.app_status import AppStatus
from reqres_app.models.user_model import User

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK)
def get_root():
    return {"message": "Welcome to your FastAPI microservice!"}


def read_users_from_file():
    users = []
    data_file_path = os.path.join(os.path.dirname(__file__), "data.txt")
    if os.path.exists(data_file_path):
        with open(data_file_path, "r") as f:
            for line in f:
                id, name, email = line.strip().split(",")
                users.append(User(id=int(id), name=name, email=email))
    else:
        print(f"File {data_file_path} does not exist.")
    return users


users = read_users_from_file()


def write_users_to_file(users):
    data_file_path = os.path.join(os.path.dirname(__file__), "data.txt")
    with open(data_file_path, "w") as f:
        for user in users:
            f.write(f"{user.id},{user.name},{user.email}\n")


@app.get("/status", status_code=HTTPStatus.OK)
async def status() -> AppStatus:
    return AppStatus(users=bool(users))


@app.get("/api/users/", status_code=HTTPStatus.OK)
async def get_users() -> Page[User]:
    return paginate(users)


add_pagination(app)


@app.get("/api/users/{user_id}", status_code=HTTPStatus.OK)
async def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="User ID is invalid")
    if user_id > len(users):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return users[user_id - 1]


@app.post("/api/users/", status_code=HTTPStatus.CREATED)
async def create_user(user: User):
    new_user = User(id=len(users) + 1, name=user.name, email=user.email)
    users.append(new_user)
    write_users_to_file(users)
    return new_user


@app.patch("/api/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def update_user(user_id: int, user: User):
    for i, u in enumerate(users):
        if u.id == user_id:
            u.name = user.name
            u.email = user.email
            write_users_to_file(users)
            return u
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/api/users/{user_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            write_users_to_file(users)
            return
    raise HTTPException(status_code=404, detail="User not found")
