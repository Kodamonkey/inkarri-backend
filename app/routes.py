from flask import Flask
from app.adapters.controllers.client_controller import client_controller

app = Flask(__name__)
app.register_blueprint(client_controller)

if __name__ == "__main__":
    app.run(debug=True)
