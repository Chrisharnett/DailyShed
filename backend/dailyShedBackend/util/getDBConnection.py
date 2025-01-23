import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def getDBConnection():
    try:
        return pymysql.connect(
            host=os.environ['HOST_ENDPOINT'],
            user=os.environ['RDS_USERNAME'],
            password=os.environ['RDS_PASSWORD'],
            db=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.InternalError as e:
        if e.args[0] == 1049:
            print("Database does not exist.")
        else:
            raise
    except pymysql.err.OperationalError as e:
        print("Operational Error:", e)
    except Exception as e:
        print("An error occurred:", e)

