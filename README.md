# Home Security System Backend

This is the backend for a home security system application, built with Flask. It provides user authentication, camera management, system arm/disarm functionality, and a basic dashboard. The application is containerized using Docker for easy deployment.

## Prerequisites

### For Local Development:
*   Python 3.8+
*   pip (Python package installer)
*   Virtual environment tool (e.g., `venv`)

### For Docker Deployment:
*   Docker installed and running on your system.

## Local Development Setup

1.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory (it's in `.gitignore` so it won't be committed). Add the following, replacing with your actual values for development:
    ```env
    SECRET_KEY='your_development_secret_key'
    DATABASE_URL='sqlite:///app.db' # Or your preferred development database URI
    FLASK_APP='run:app'
    FLASK_ENV='development' # Enables debug mode
    ```
    *Note: `FLASK_APP` and `FLASK_ENV` can also be set directly in your terminal. The `.env` file is loaded by `python-dotenv` if you run `flask run` or implicitly by Flask in development.*

5.  **Initialize and migrate the database:**
    If this is the first time, or if there are new migrations:
    ```bash
    # Ensure FLASK_APP is set, e.g., export FLASK_APP=run:app or it's in .flaskenv/.env
    flask db init  # Only if migrations folder doesn't exist
    flask db migrate -m "Initial migration" # Or a descriptive message for new changes
    flask db upgrade
    ```

6.  **Run the application:**
    ```bash
    flask run
    ```
    Or using the `run.py` script (which also enables debug mode as currently written):
    ```bash
    python run.py
    ```
    The application should be accessible at `http://127.0.0.1:5000/`.

## Docker Setup

### Building the Docker Image
1.  Navigate to the root directory of the project (where the `Dockerfile` is located).
2.  Run the following command to build the image. Replace `home-security-backend` with your preferred image name:
    ```bash
    docker build -t home-security-backend .
    ```

### Running the Docker Container
1.  Once the image is built, run it as a container:
    ```bash
    docker run -p 5000:5000 --name home-security-app home-security-backend
    ```
    *   `-p 5000:5000`: Maps port 5000 on your host to port 5000 in the container.
    *   `--name home-security-app`: (Optional) Assigns a name to your container.

2.  **Environment Variables for Production with Docker:**
    When running in production, pass environment variables for sensitive data. The `FLASK_ENV=production` is already set in the Dockerfile.
    ```bash
    docker run -p 5000:5000 \
          -e SECRET_KEY="your_very_strong_and_random_production_secret_key" \
          -e DATABASE_URL="your_production_database_uri" \
          --name home-security-app-prod home-security-backend
    ```
    *   **Database Persistence:** For SQLite, if you want to persist the database outside the container, use Docker volumes. Example (assuming `DATABASE_URL` inside the container is `sqlite:////app/instance/prod.db`):
        ```bash
        # Ensure your config.py uses a path like 'sqlite:///instance/prod.db' for DATABASE_URL
        # when using this volume mounting strategy.
        docker run -p 5000:5000 \
              -e SECRET_KEY="your_production_secret_key" \
              -e DATABASE_URL="sqlite:////app/instance/prod.db" \
              -v /path/on/your/host/data:/app/instance \
              --name home-security-app-prod home-security-backend
        ```
        For production, a more robust database (e.g., PostgreSQL) is recommended over SQLite.

### Accessing the Application
*   Once the container is running, the application should be accessible at `http://localhost:5000`.

---
