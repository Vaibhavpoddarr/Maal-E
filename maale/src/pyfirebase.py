import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('biodome-34fc6-firebase-adminsdk-dqk1w-6df9926feb.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://biodome-34fc6-default-rtdb.firebaseio.com"
})

ref = db.reference("/DHT11/Temperature")
print(ref.get())


