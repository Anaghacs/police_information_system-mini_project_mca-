from flask import Flask
from public import public
from admin import admin
from station import station
from user import user

app=Flask(__name__)
app.secret_key="a"
app.register_blueprint(public)
app.register_blueprint(admin)
app.register_blueprint(station)
app.register_blueprint(user)
app.run(debug=True, port=5018)


	