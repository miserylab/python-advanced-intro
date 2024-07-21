Here is the README.md in Markdown format:

# Microservice and API Autotests
=====================================

## Introduction
This repository contains a Python + FastAPI microservice and API autotests for the "QA.QURU Python Advanced Intro" course.

## Microservice
### Endpoints

The microservice provides the following API endpoints:

* `GET /api/users`: Returns a list of all users
* `GET /api/users/{user_id}`: Returns a single user by ID
* `POST /api/users`: Creates a new user
* `PUT /api/users/{user_id}`: Updates an existing user
* `DELETE /api/users/{user_id}`: Deletes a user

### Data Storage
The microservice stores data in a text file for now, but will be migrated to a database in future iterations.

## API Autotests
### Scenarios

The API autotests cover the following scenarios:

* Successful creation of a new user
* Successful retrieval of a single user by ID
* Successful retrieval of a list of users
* Successful update of an existing user
* Successful deletion of a user

### Test Data
The test data is generated using the Faker library and is stored in the reqres_tests/utils directory.

## Running the Microservice
### Command

To run the microservice execute the following command:
```
uvicorn reqres_app.main:app --reload
```
This will start the microservice on `http://localhost:8000`.

## Running the Autotests
### Command

To run the autotests execute the following command:
```
pytest
```

## Code Organization
### Directories

The code is organized into the following directories:

* `reqres_app`: Contains the FastAPI microservice code and the text file storing user data
* `reqres_tests/utils`: Contains utility files for test data generation
* `tests`: Contains the API autotests