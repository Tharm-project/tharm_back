import firebase_admin

from firebase_admin import credentials, auth

cred = credentials.Certificate("./firebase_key.json")
default_app = firebase_admin.initialize_app(cred)

print(default_app.name)