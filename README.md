# Instagram Clone - Local Development Setup

This document outlines the steps to set up and run the Instagram Clone application on your local machine for development purposes.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Docker:** [https://www.docker.com/get-started](https://www.docker.com/get-started)
*   **Docker Compose:** Usually included with Docker Desktop.  If not, refer to the Docker documentation for installation instructions.
*   **Python 3.7+:** [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   **pip:** Python package installer (usually included with Python).

## Setup Instructions

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd <your_repository_directory>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install backend dependencies:**

    ```bash
    cd backend
    pip install -r requirements.txt
    cd ..
    ```

4.  **Run the application using Docker Compose:**

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images for the backend and frontend services and start them.  The first time you run this, it may take a few minutes to download the necessary images and build the application.

5.  **Access the application:**

    *   **Frontend:** Open your web browser and navigate to `http://localhost:8080`.
    *   **Backend (API):** The API endpoints are available at `http://localhost:8000`.  You can use tools like `curl`, `httpie`, or Postman to test the API.

## Database Setup

The application uses a PostgreSQL database defined in the `docker-compose.yml` file. The database credentials are:

*   **User:** example
*   **Password:** example
*   **Database:** instagram

The backend is configured to connect to this database using the `DATABASE_URL` environment variable.

**Note:** The initial setup uses SQLite. If you wish to use PostgreSQL, ensure the `DATABASE_URL` in `docker-compose.yml` and `SQLALCHEMY_DATABASE_URL` in `backend/database.py` are correctly configured for PostgreSQL and that you have installed the `psycopg2-binary` driver: `pip install psycopg2-binary`.

## Running Tests

To run the backend tests:

1.  Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2.  Run the tests using `pytest`:

    ```bash
    pytest
    ```

## Development

Make your code changes, and the application should automatically reload (due to the volumes mounted in `docker-compose.yml`).

## Stopping the Application

To stop the application, run:
```
docker-compose down
```
