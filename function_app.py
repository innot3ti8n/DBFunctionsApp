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

# GET: Get Criteria list for a skill
'''

    Route: '/criteria/{skillId:int?}'
    Route Params: {
        skillId: Int. Values are 1: Punctuation, 2: Vocabulary, 3: Cohesion, 4: Sentente Type & Structure, 5: Developing & Elaborating Ideas
    }
'''
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

# GET: Get Text Component for a Specific Skill
'''
    Param: skillId (1: Punctuation, 2: Vocabulary, 3: Cohesion, 4: Sentente Type & Structure, 5: Developing & Elaborating Ideas)
    Route: text_component/{skillId:int?}
'''
@app.route(route="text_component/{skillId:int?}", methods=["GET"])
def textComponent(req: func.HttpRequest) -> func.HttpResponse:
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

    query = f"select * from text_component WHERE skill_id={id};"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=200)
    finally:
        conn.close()

# POST: Send new Annotation Text Sample to DB 
# Request Body
'''
{
    "text": String,
    "annotationType": Number,
    "sampleId": Number,
}
'''
@app.route(route="text_sample_annotation", methods=["POST"])
def sendTextSampleAnnotation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_json()

    try:
            body = req.get_json()
            textSampleContent = body["text"]
            annotatationType = body["annotationType"]
            textSampleId = body["sampleId"]
            skillLevelId = body["skillLevelId"] if "skillLevelId" in body.keys() else 0
    except ValueError:
            print(f"Invalid Request body, {ValueError}")

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

    query = f"Insert into text_sample_annotation SET text_sample_id={textSampleId}, annotation_type_id={annotatationType}, text='{textSampleContent}';"

    try:
        cursor.execute(query)
        conn.commit()
        result = cursor.lastrowid
        
        if(skillLevelId != 0):
            query = f"Insert into results SET text_sample_annotation_id={result}, skill_level_id={skillLevelId}"
            cursor.execute(query)
            conn.commit()

        return func.HttpResponse(json.dumps(result), status_code=200)
    finally:
        conn.close()

# GET: Get Annotation Text Sample
'''
route: '/text_sample_annotation/{text_sample_annotation_id:int?}'
Param: text_sample_annotation_id: Int
'''
@app.route(route="text_sample_annotation/{text_sample_annotation_id:int?}", methods=["GET"])
def getTextSampleAnnotation(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    id = req.route_params.get('text_sample_annotation_id')

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

    query = f"SELECT * from text_sample_annotation WHERE text_sample_annotation_id={id};"

    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            return func.HttpResponse(json.dumps(result), status_code=200)
        else:
            return func.HttpResponse(None, status_code=200)
    finally:
        conn.close()


# POST: Text Sample Create New (student_name)
# Route: '/text_sample'
# Request Body
'''
{
    "student_name": String,
}
'''
@app.route(route="text_sample", methods=["POST"])
def sendTextSample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_json()

    try:
            body = req.get_json()
            studentName = body["student_name"]
    except ValueError:
            print(f"Invalid Request body, {ValueError}")

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

    query = f"Insert into text_sample (student_name) VALUES ('{studentName}');"

    try:
        cursor.execute(query, multi=True)
        conn.commit()
        result = cursor.lastrowid
        return func.HttpResponse(json.dumps(result), status_code=200)
    finally:
        conn.close()