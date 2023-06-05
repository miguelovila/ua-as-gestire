# Gestire - Room and Equipment Management System

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Frontend](#frontend)
- [Backend](#backend-1)
  - [Authentication Routes](#authentication-routes)
  - [Room Routes](#room-routes)
  - [Equipment Routes](#equipment-routes)
  - [User Routes](#users)

## Introduction

Gestire is a room and equipment management system that allows users to book rooms and equipment for their classes and events. The system is designed to be used by the staff and students of the School of DETI-UA. The system is composed of a web application, mobile application, a REST API and a hardware component.

## Getting Started

### Prerequisites

#### Backend (Recommended)

- Any operating system that supports Python 3.11.\* and the required dependencies.
- [Python 3.11.\*](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)
- [bcrypt](https://pypi.org/project/bcrypt/)

#### Frontend

- Any operating system that supports a web browser.

### Installation

#### Backend (Recommended)

In order to install all the necessary dependencies, run the following command:

```bash
pip install -r requirements.txt
```

#### Frontend

No installation is required for the frontend.

### Running the Application

#### Backend

In order to run the server, run the following command:

```bash
python app.py
```

> **Note:** The server will be running on port 5000 by default.

> If you have nodemon installed (recommended), you can run the following command instead:
>
> ```bash
> nodemon app.py
> ```

#### Frontend

For the webapp, no installation is required for the frontend.

For the mobile app, you can download the APK file from the releases page and install it on your Android device.

## Frontend

This frontend is written in flutter and dart. Follows material design 3 guidelines and is responsive to different screen sizes.

## Backend

This section describes the backend of the application, including the API routes and the database schema.

### POST /api/auth

Authenticates a user with the specified email and password.

#### Request Body

| Field    | Type   | Required | Description          |
| -------- | ------ | -------- | -------------------- |
| email    | string | Yes      | The user's email.    |
| password | string | Yes      | The user's password. |

#### Response

##### Success

If the authentication is successful, the server will respond with a 200 OK status code and a JSON object containing the user's information and token:

```json
{
  "mec": "<user_mec>",
  "name": "<user_name>",
  "email": "<user_email>",
  "profile_picture": "<user_profile_picture>",
  "token": "<user_token>"
}
```

##### Error

If the authentication fails, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                       | Description                                             |
| ----------- | ----------------------------- | ------------------------------------------------------- |
| 401         | Invalid username or password. | The email or password provided is invalid.              |
| 401         | Invalid request.              | The request is missing required fields or is malformed. |
| 500         | Internal server error.        | An internal server error occurred.                      |

### POST /api/auth/check

Checks the validity of a token.

#### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| token | string | Yes      | The user's token. |

#### Response

##### Success

If the token is valid and has not expired, the server will respond with a 200 OK status code and a JSON object indicating that the token is valid:

```json
{
  "valid": true
}
```

##### Error

If the token is invalid or has expired, the server will respond with an appropriate error status code and a JSON object indicating that the token is invalid:

```json
{
  "valid": false
}
```

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Invalid token.         | The token provided is invalid or has expired.           |
| 401         | Invalid request.       | The request is missing required fields or is malformed. |
| 500         | Internal server error. | An internal server error occurred.                      |

## Room Routes

### POST /api/rooms

Filters and retrieves rooms based on specified parameters.

#### Request Body

| Field           | Type    | Required | Description                                                      |
| --------------- | ------- | -------- | ---------------------------------------------------------------- |
| token           | string  | Yes      | The user's token.                                                |
| filters         | object  | Yes      | The filter parameters for the rooms.                             |
| minSeats        | number  | No       | The minimum number of seats required in the rooms.               |
| minPowerSockets | number  | No       | The minimum number of power sockets required in the rooms.       |
| type            | string  | No       | The type of room to filter (description field).                  |
| availableNow    | boolean | No       | Flag indicating whether to filter for currently available rooms. |

#### Response

##### Success

If the rooms are successfully filtered, the server will respond with a 200 OK status code and a JSON object containing the filtered rooms:

```json
{
  "rooms": [
    {
      "id": 1,
      "name": "Room 1",
      "description": "Meeting Room",
      "capacity": 10,
      "power_sockets": 6,
      "computers": 0,
      "oscilloscopes": 0,
      "signal_generators": 0,
      "multimeters": 0,
      "sound_system": true,
      "projector": true,
      "whiteboard": true
    },
    {
      "id": 2,
      "name": "Room 2",
      "description": "Classroom",
      "capacity": 20,
      "power_sockets": 12,
      "computers": 10,
      "oscilloscopes": 2,
      "signal_generators": 2,
      "multimeters": 5,
      "sound_system": true,
      "projector": true,
      "whiteboard": true
    }
  ]
}
```

##### Error

If there are errors in the request or no rooms are found with the specified parameters, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The user's token is invalid or expired.                 |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 400         | No rooms found.        | No rooms found with the specified parameters.           |
| 500         | Internal server error. | An internal server error occurred.                      |

### GET /api/rooms/{room_id}

Retrieves details of a specific room.

#### Request Parameters

| Parameter | Type | Required | Description         |
| --------- | ---- | -------- | ------------------- |
| room_id   | int  | Yes      | The ID of the room. |

#### Response

##### Success

If the room is found, the server will respond with a 200 OK status code and a JSON object containing the room details:

```json
{
  "room": {
    "id": 1,
    "name": "Room 1",
    "description": "Meeting Room",
    "capacity": 10,
    "power_sockets": 6,
    "computers": 0,
    "oscilloscopes": 0,
    "signal_generators": 0,
    "multimeters": 0,
    "sound_system": true,
    "projector": true,
    "whiteboard": true
  }
}
```

##### Error

If the room is not found or there are errors in

the request, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The user's token is invalid or expired.                 |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 400         | Room not found.        | The specified room ID does not exist.                   |
| 500         | Internal server error. | An internal server error occurred.                      |

### POST /api/rooms/{room_id}/reserve

Reserves a specific room for a specified time period.

#### Request Parameters

| Parameter | Type | Required | Description         |
| --------- | ---- | -------- | ------------------- |
| room_id   | int  | Yes      | The ID of the room. |

#### Request Body

| Field      | Type   | Required | Description                                         |
| ---------- | ------ | -------- | --------------------------------------------------- |
| token      | string | Yes      | The user's token.                                   |
| start_time | number | Yes      | The start time of the reservation (Unix timestamp). |
| duration   | number | Yes      | The duration of the reservation in seconds.         |
| reason     | string | No       | The reason for the reservation (optional).          |

#### Response

##### Success

If the room is successfully reserved, the server will respond with a 200 OK status code and a JSON object containing a success message:

```json
{
  "success": "Room reserved"
}
```

##### Error

If there are errors in the request or the room is not available for the specified time period, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                   | Description                                              |
| ----------- | ------------------------- | -------------------------------------------------------- |
| 401         | Access denied.            | The user's token is invalid or expired.                  |
| 400         | Invalid request.          | The request is missing required fields or is malformed.  |
| 400         | Invalid reservation time. | The specified reservation time is invalid.               |
| 400         | Room not available.       | The specified room is not available for the reservation. |
| 500         | Internal server error.    | An internal server error occurred.                       |

## Equipment Routes

### POST /api/equipments

Retrieves a list of equipments based on specified filters.

#### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| token | string | Yes      | The user's token. |

#### Response

##### Success

If the equipments are successfully retrieved, the server will respond with a 200 OK status code and a JSON object containing the list of equipments:

```json
{
  "equipments": [
    {
      "id": 1,
      "name": "Equipment 1",
      "description": "Equipment description",
      "locker": "Locker 1",
      "initial_date": "2023-06-01",
      "final_date": "2023-06-10"
    },
    {
      "id": 2,
      "name": "Equipment 2",
      "description": "Equipment description",
      "locker": "Locker 2",
      "initial_date": "2023-06-05",
      "final_date": "2023-06-15"
    }
  ]
}
```

##### Error

If there are errors in the request or no equipments are found, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The user's token is invalid or expired.                 |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 400         | No equipments found.   | No equipments found with the specified parameters.      |
| 500         | Internal server error. | An internal server error occurred.                      |

### POST /api/equipments/{equipment_id}

Retrieves details of a specific equipment.

#### Request Parameters

| Parameter    | Type | Required | Description              |
| ------------ | ---- | -------- | ------------------------ |
| equipment_id | int  | Yes      | The ID of the equipment. |

#### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| token | string | Yes      | The user's token. |

#### Response

##### Success

If the equipment is found, the server will respond with a 200 OK status code and a JSON object containing the equipment details:

```json
{
  "equipment": {
    "id": 1,
    "name": "Equipment 1",
    "description": "Equipment description",
    "locker": "Locker 1",
    "initial_date": "2023-06-01",
    "final_date": "2023-06-10"
  }
}
```

##### Error

If the equipment is not found or there are errors in the request, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The user's token is invalid or expired.                 |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 400         | Equipment not found.   | The specified equipment ID does not exist.              |
| 500         | Internal server error. | An internal server error occurred.                      |

### POST /api/equipments/{equipment_id}/reserve

Reserves a specific equipment for a specified time period.

#### Request Parameters

| Parameter    | Type | Required | Description |
| ------------ | ---- | -------- | ----------- |
| equipment_id |

int | Yes | The ID of the equipment. |

#### Request Body

| Field    | Type   | Required | Description                                 |
| -------- | ------ | -------- | ------------------------------------------- |
| token    | string | Yes      | The user's token.                           |
| duration | number | Yes      | The duration of the reservation in seconds. |
| reason   | string | No       | The reason for the reservation (optional).  |

#### Response

##### Success

If the equipment is successfully reserved, the server will respond with a 200 OK status code and a JSON object containing a success message and a reservation code:

```json
{
  "message": "Equipment reserved",
  "code": 123456
}
```

##### Error

If there are errors in the request, the equipment is not available, or there are issues with the reservation process, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                  | Description                                               |
| ----------- | ------------------------ | --------------------------------------------------------- |
| 401         | Access denied.           | The user's token is invalid or expired.                   |
| 400         | Invalid request.         | The request is missing required fields or is malformed.   |
| 400         | Equipment not available. | The specified equipment is not available for reservation. |
| 500         | Internal server error.   | An internal server error occurred.                        |

### POST /api/equipments/{equipment_id}/return

Returns a specific equipment.

#### Request Parameters

| Parameter    | Type | Required | Description              |
| ------------ | ---- | -------- | ------------------------ |
| equipment_id | int  | Yes      | The ID of the equipment. |

#### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| token | string | Yes      | The user's token. |

#### Response

##### Success

If the equipment return process is successful, the server will respond with a 200 OK status code and a JSON object containing a success message and a return code:

```json
{
  "message": "Equipment return code",
  "code": 123456
}
```

##### Error

If there are errors in the request, the equipment is not available for return, or there are issues with the return process, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                             | Description                                             |
| ----------- | ----------------------------------- | ------------------------------------------------------- |
| 401         | Access denied.                      | The user's token is invalid or expired.                 |
| 400         | Invalid request.                    | The request is missing required fields or is malformed. |
| 400         | Equipment not available for return. | The specified equipment is not available for return.    |
| 500         | Internal server error.              | An internal server error occurred.                      |

## Users

### POST /api/users/reservations

Retrieves reservations for a user based on their token.

#### Request Body

| Field | Type   | Required | Description       |
| ----- | ------ | -------- | ----------------- |
| token | string | Yes      | The user's token. |

#### Response

##### Success

If the reservations are successfully retrieved, the server will respond with a 200 OK status code and a JSON object containing the user's reservations:

```json
{
  "reservations": {
    "rooms": [
      {
        "id": 1,
        "start_time": 1667856000,
        "end_time": 1667863200,
        "room": {
          "id": 1,
          "name": "Room 1",
          "capacity": 10,
          "available": true
        }
      },
      {
        "id": 2,
        "start_time": 1667900400,
        "end_time": 1667907600,
        "room": {
          "id": 2,
          "name": "Room 2",
          "capacity": 20,
          "available": true
        }
      }
    ],
    "equipments": [
      {
        "id": 1,
        "start_time": 1667856000,
        "end_time": 1667863200,
        "equipment": {
          "id": 1,
          "name": "Equipment 1",
          "available": true
        }
      },
      {
        "id": 2,
        "start_time": 1667900400,
        "end_time": 1667907600,
        "equipment": {
          "id": 2,
          "name": "Equipment 2",
          "available": true
        }
      }
    ]
  }
}
```

##### Error

If there are errors in the request or no reservations are found for the user, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The user's token is invalid or expired.                 |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 404         | No reservations found. | No reservations found for the user.                     |
| 500         | Internal server error. | An internal server error occurred.                      |

## Locker Route

### POST /api/locker/{code}

Gets the locker associated with a code.

#### Request Parameters

| Parameter | Type | Required | Description      |
| --------- | ---- | -------- | ---------------- |
| code      | int  | Yes      | The locker code. |

#### Request Body

| Field | Type   | Required | Description              |
| ----- | ------ | -------- | ------------------------ |
| token | string | Yes      | The locker secret token. |

#### Response

##### Success

If the locker code is valid and associated with an equipment, the server will respond with a 200 OK status code and a JSON object containing the locker information:

```json
{
  "type": "get",
  "locker": "Locker 1"
}
```

or

```json
{
  "type": "put",
  "locker": "Locker 2"
}
```

The `type` field indicates whether the code is associated with a "get" or "put" action.

##### Error

If there are errors in the request, the code is invalid, or there are issues with the locker retrieval process, the server will respond with an appropriate error status code and an error message:

| Status Code | Message                | Description                                             |
| ----------- | ---------------------- | ------------------------------------------------------- |
| 401         | Access denied.         | The locker secret token is invalid.                     |
| 400         | Invalid request.       | The request is missing required fields or is malformed. |
| 400         | Invalid code.          | The specified code is invalid or expired.               |
| 500         | Internal server error. | An internal server error occurred.                      |
