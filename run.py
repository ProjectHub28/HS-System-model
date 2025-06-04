from app import create_app, db
from app.models import User # Ensure models are imported for migrations

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
