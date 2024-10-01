import azure.functions as func
import logging
import mysql.connector
import os
from mysql.connector import errorcode

dbConfig = {
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_DB'],
    'user': os.environ['DB_USR'],
    'password': os.environ['DB_PWD'],
    'ssl_ca': 'DigiCertGlobalRootCA.pem',
    'ssl_disabled' : False
}

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="criteria/{skillId:int?}", methods=["GET"])
def criteria(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('id')

    try:
        conn = mysql.connector.connect(**dbConfig)
        logging.info("Connection Established")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with the username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = conn.cursor()

    query = f"SELECT FROM TABLE WHERE skill_id = {id};"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(result, 200)
        else:
            return func.HttpResponse(None, 200)
    finally:
        conn.close()
