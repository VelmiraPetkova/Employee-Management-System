# Employee Management System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
  - [1. User Registration](#1-user-registration)
  - [2. Creating a Contract](#2-creating-a-contract)
  - [3. Managing Absences](#3-managing-absences)
- [Contributing](#contributing)


## Introduction
This platform allows users to register themselves in the system, view information about their contracts, and submit requests for sick leave and vacation. It enables accountants and managers to create employment contracts and track/manage absences. It can be used in organizational contexts where absence tracking and contract management are essential, such as human resources systems or employee management platforms.

## Features
- **User Registration**: Sign up users with unique credentials, validate user input, and store securely.
- **Contract Creation**: Create and manage contracts between users and the system.
- **Absence Management**: Allow users to report, track, and manage absences.

## Technologies
- **Backend**: Python, Flask
- **Database**: PostgresSQL, AWS S3
- **Authentication**: JWT (JSON Web Tokens)
- **Other**: Postman for API testing, Pytest, SES-AWS 

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/VelmiraPetkova/Employee-Management-System/.git
   ```
2. Navigate to the project directory:
   ```bash
   cd  Employee-Management-System ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the root directory with the following keys:
     ```plaintext
	DB_USER=postgres-user
	DB_PASSWORD=password
	DB_HOST=127.0.0.1
	DB_PORT=5432
	DB_NAME=payrollsystem     
    JWT_SECRET=your_secret_key
     ```
5. Start the server:
   ```bash
   flask run
   ```

## API Endpoints Examples with Postman

### 1. User Registration
- **Endpoint**: `POST /register`
- **URL**: `http://127.0.0.1:5000/register`
- **Description**: Register a new user.
- **Postman Setup**:
  - **Method**: POST
  - **Body**: JSON (raw)
    ```json
    {
    "name": "Testname Example",
    "civil_number": "1111111111",
    "phone": "08811111",
    "iban": "BG70BNBG47622021445672",
    "email": "email.example@gmail.com",
    "password": "Password-example1"    
     }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`

### 2. User Login
- **Endpoint**: `POST /login`
- **URL**: `http://127.0.0.1:5000/login`
- **Description**: Log in an existing user.
- **Postman Setup**:
  - **Method**: POST
  - **Body**: JSON (raw)
    ```json
    {
      "username": "example_user",
      "password": "example_password"
    }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`


### 3. Contracts register
- **Endpoint**: `POST /contract`
- **URL**: `http://127.0.0.1:5000/contract`
- **Description**: Create or manage a contract.This method requires that your role in the system is Accountant
- **Postman Setup**:
  - **Method**: POST
  - **Body**: JSON (raw)
    ```json
    {
          "employee": 1,
          "effective": "2024-10-14",
          "salary": 1000,
          "hours": 8,
          "department": "example_department",
          "position": "example_position"
    }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`


### 4. Review your contract
- **Endpoint**: `GET /contract`
- **URL**: `http://127.0.0.1:5000/contract`
- **Description**: Review your contract, or the contract of your employees.
- **Postman Setup**:
  - **Method**: POST
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`



### 5. Absence Registration
- **Endpoint**: `POST /absenceregister`
- **URL**: `http://127.0.0.1:5000/absenceregister`
- **Description**: Register a new absence.
- **Postman Setup**:
  - **Method**: POST
  - **Body**: JSON (raw)
    ```json
    {
      "from_": "2024-10-20",
      "to_": "2024-10-20",
      "days": "2",
      "employee": "2",
      "type": "sick",
      "photo":"/9j/4AAQSkZJRgABAQAAAQABAAD/…",
      "photo_extension":"jpeg"

    }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`


### 6. Assign Manager to User
- **Endpoint**: `PUT /addmanager/user/<int:user_id>`
- **URL**: `http://127.0.0.1:5000/addmanager/user/1`
- **Description**: Assign a manager to a specified user.
- **Postman Setup**:
  - **Method**: PUT
  - **Body**: JSON (raw)
    ```json
    {
      "manager_id": 2
    }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`

### 7. Approve Absence
- **Endpoint**: `GET /absences/<int:absence_id>/approve`
- **URL**: `http://127.0.0.1:5000/absences/1/approve`
- **Description**: Approve a pending absence request.
- **Postman Setup**:
  - **Method**: PUT
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`

### 8. Reject Absence
- **Endpoint**: `GET /absences/<int:absence_id>/reject`
- **URL**: `http://127.0.0.1:5000/absences/1/reject`
- **Description**: Reject a pending absence request.
- **Postman Setup**:
  - **Method**: PUT
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`

### 9. Change Contract Details
- **Endpoint**: `PUT /change/<int:contract_id>/contract`
- **URL**: `http://127.0.0.1:5000/change/1/contract`
- **Description**: Update details of an existing contract.
- **Postman Setup**:
  - **Method**: PUT
  - **Body**: JSON (raw)
    ```json
    {
      "position": "Lead Developer"
    }
    ```
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`

### 9. Delete Absence
- **Endpoint**: `DELETE /absences/<int:absence_id>/delete`
- **URL**: `http://127.0.0.1:5000/absences/1/delete`
- **Description**: Delete an absence record.
- **Postman Setup**:
  - **Method**: DELETE
  - **Headers**: 
    - `Content-Type`: `application/json`
    - `Authorization`: `Bearer`


