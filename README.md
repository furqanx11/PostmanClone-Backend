# PostmanClone-Backend

PostmanClone-Backend is a FastAPI-based backend application designed to manage collections of HTTP requests, similar to Postman. This project includes JWT authentication, database interactions using Tortoise ORM, and various utility functions to support the application's functionality.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)

## Features

- **JWT Authentication**: Secure user authentication using JSON Web Tokens.
- **Database Integration**: Uses Tortoise ORM for database interactions.
- **Modular Architecture**: Organized code structure with routers, schemas, and utilities.
- **CORS Middleware**: Configurable CORS settings for cross-origin requests.
- **Custom Exception Handling**: Custom validation and exception handling.

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/PostmanClone-Backend.git
    cd PostmanClone-Backend
    ```

2. **Create and activate a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    Configure your database settings in `config.py` and run migrations:


## Configuration

Create a `.env` file in the root directory and configure environment variables:
