# main.py
from flask import Flask
from infrastructure.database import db
from adapters.controllers.user_controller import user_controller

app = Flask(__name__)
# Load configuration from environment variables or a config file
# For example, using a PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@hostname/database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(user_controller, url_prefix='/users')

if __name__ == "__main__":
    app.run(debug=True)
