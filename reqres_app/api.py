import os

from fastapi import FastAPI, HTTPException

from reqres_app.models import User

app = FastAPI()


@app.get("/")
def read_root():
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


@app.get("/api/users/")
async def read_users():
    return users


@app.get("/api/users/{user_id}")
async def read_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/api/users/")
async def create_user(user: User):
    new_user = User(id=len(users) + 1, name=user.name, email=user.email)
    users.append(new_user)
    write_users_to_file(users)
    return new_user


@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user: User):
    for i, u in enumerate(users):
        if u.id == user_id:
            u.name = user.name
            u.email = user.email
            write_users_to_file(users)
            return u
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            del users[i]
            write_users_to_file(users)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
