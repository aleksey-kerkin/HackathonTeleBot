import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
DB_NAME = "vacation_planner.db"
TABLE_NAME = "users"
