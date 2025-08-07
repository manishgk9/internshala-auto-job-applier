import os
from dotenv import load_dotenv

load_dotenv()
internshala_credentials = {
    "email": os.getenv("EMAIL"),
    "password": os.getenv("PASSWORD"),
    "token":os.getenv("GIMINI_API_KEY")
    }
