from flask import Flask
from app.routes import auth

app = Flask(__name__)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run(debug=True)
