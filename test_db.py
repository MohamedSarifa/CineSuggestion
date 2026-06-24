from app import app
from database import db

with app.app_context():

    try:
        db.session.execute(
            db.text("SELECT 1")
        )

        print("Database Connected Successfully")

    except Exception as e:
        print(e)