import azure.functions as func
import logging
import mysql.connector
import os
from mysql.connector import errorcode
import json

dbConfig = {
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_DB'],
    'user': os.environ['DB_USR'],
    'password': os.environ['DB_PWD'],
    'ssl_ca': './DigiCertGlobalRootCA.pem',
    'ssl_disabled' : False
}

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="criteria/{skillId:int?}", methods=["GET"])
def criteria(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('skillId')

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
            print(**dbConfig)
    else:
        cursor = conn.cursor(dictionary=True)

    query = f"select C.criteria_id, C.skill_level_id, S.level_id, C.criteria from Criteria as C inner join skill_level as S ON C.skill_level_id = S.skill_level_id WHERE skill_id = {id};"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=200)
    finally:
        conn.close()
